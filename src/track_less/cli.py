"""CLI interface for track-less."""

import shutil
import sys
import tempfile
from pathlib import Path
import click

from . import __version__
from .config import OUTPUT_DIR, AVAILABLE_STEMS
from .downloader import download_audio
from .separator import separate_stems
from .mixer import mix_stems
from .exceptions import TrackLessError, DownloadError, SeparationError, MixingError


@click.command()
@click.argument('url')
@click.option('-g', '--guitar', is_flag=True, help='Remove guitar track')
@click.option('-v', '--vocals', is_flag=True, help='Remove vocals track')
@click.option('-d', '--drums', is_flag=True, help='Remove drums track')
@click.option('-b', '--bass', is_flag=True, help='Remove bass track')
@click.option('-p', '--piano', is_flag=True, help='Remove piano track')
@click.option('--other', is_flag=True, help='Remove other instruments track')
@click.option('-s', '--stem', is_flag=True, help='Extract stems instead of mixing (saves raw stem files)')
@click.option('-P', '--preview', is_flag=True, help='Process only the first 30 seconds (quick test)')
@click.option('-o', '--output', type=click.Path(), help='Output directory (default: ~/Music/track-less)')
@click.version_option(version=__version__, prog_name='track-less')
def main(url, guitar, vocals, drums, bass, piano, other, stem, preview, output):
    """
    Remove instrument tracks from songs using AI stem separation.

    Downloads audio from YouTube/YouTube Music, separates it into individual
    instrument stems using Demucs, and mixes the stems back together excluding
    the specified instruments.

    Example:
        track-less "https://youtube.com/watch?v=..." -g
        track-less "https://music.youtube.com/watch?v=..." -g -v
    """
    try:
        # Build list of instruments to remove based on flags
        instruments_to_remove = []
        if guitar:
            instruments_to_remove.append('guitar')
        if vocals:
            instruments_to_remove.append('vocals')
        if drums:
            instruments_to_remove.append('drums')
        if bass:
            instruments_to_remove.append('bass')
        if piano:
            instruments_to_remove.append('piano')
        if other:
            instruments_to_remove.append('other')

        # Validate that at least one instrument is selected
        if not instruments_to_remove:
            action = "extract" if stem else "remove"
            click.echo(
                f"Error: Please specify at least one instrument to {action}.\n"
                "Use -g (guitar), -v (vocals), -d (drums), -b (bass), -p (piano), or --other.",
                err=True
            )
            sys.exit(1)

        # Validate instruments are recognized
        invalid_instruments = [i for i in instruments_to_remove if i not in AVAILABLE_STEMS]
        if invalid_instruments:
            click.echo(
                f"Error: Invalid instruments: {', '.join(invalid_instruments)}\n"
                f"Available: {', '.join(AVAILABLE_STEMS)}",
                err=True
            )
            sys.exit(1)

        # Setup output directory
        output_dir = Path(output) if output else OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)

        click.echo(f"track-less v{__version__}")
        if stem:
            click.echo(f"Extracting stems: {', '.join(instruments_to_remove)}")
        else:
            click.echo(f"Removing: {', '.join(instruments_to_remove)}")
        if preview:
            click.echo("Preview mode: first 30 seconds only")
        click.echo(f"Output directory: {output_dir}\n")

        # Use temporary directory for intermediate files
        with tempfile.TemporaryDirectory(prefix="track-less-") as temp_dir:
            temp_path = Path(temp_dir)

            # Step 1: Download audio from YouTube
            click.echo("Step 1/3: Downloading audio from YouTube...")
            try:
                audio_file, title = download_audio(url, str(temp_path), preview=preview)
                click.echo(f"✓ Downloaded: {title}\n")
            except DownloadError as e:
                click.echo(f"✗ Download failed: {str(e)}", err=True)
                sys.exit(1)

            # Step 2: Separate stems using Demucs
            click.echo("Step 2/3: Separating stems with Demucs (this may take several minutes)...")
            click.echo("Note: First run will download the htdemucs_6s model (~2GB)")
            try:
                stems_dir = separate_stems(audio_file, str(temp_path))
                click.echo(f"✓ Separated into {len(AVAILABLE_STEMS)} stems\n")
            except SeparationError as e:
                click.echo(f"✗ Separation failed: {str(e)}", err=True)
                sys.exit(1)

            # Step 3: Extract stems or mix
            if stem:
                click.echo("Step 3/3: Extracting stems...")
                output_files = []
                for instrument in instruments_to_remove:
                    src = stems_dir / f"{instrument}.wav"
                    dst = output_dir / f"{title}_{instrument}.wav"
                    shutil.copy2(src, dst)
                    output_files.append(dst)
                click.echo(f"✓ Extracted {len(output_files)} stem(s)\n")
            else:
                click.echo("Step 3/3: Mixing stems...")
                try:
                    output_file = mix_stems(
                        stems_dir,
                        instruments_to_remove,
                        output_dir,
                        title
                    )
                    click.echo(f"✓ Mixed successfully\n")
                except MixingError as e:
                    click.echo(f"✗ Mixing failed: {str(e)}", err=True)
                    sys.exit(1)

        # Success!
        click.echo("=" * 60)
        click.echo("Success! Output saved to:")
        if stem:
            for f in output_files:
                click.echo(f"  {f}")
        else:
            click.echo(f"  {output_file}")
        click.echo("=" * 60)

    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user", err=True)
        sys.exit(130)
    except TrackLessError as e:
        click.echo(f"\nError: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\nUnexpected error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

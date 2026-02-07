"""Audio mixing utilities."""

from pathlib import Path
import re
import numpy as np
import soundfile as sf

from .config import AVAILABLE_STEMS, NORMALIZATION_HEADROOM
from .exceptions import MixingError


def mix_stems(
    stems_dir: Path,
    instruments_to_remove: list[str],
    output_dir: Path,
    title: str
) -> Path:
    """
    Mix stems together, excluding specified instruments.

    Args:
        stems_dir: Directory containing separated stem files
        instruments_to_remove: List of instrument names to exclude from mix
        output_dir: Directory to save the mixed output
        title: Song title for output filename

    Returns:
        Path to the mixed output file

    Raises:
        MixingError: If mixing fails
    """
    try:
        # Determine which stems to include in the mix
        stems_to_include = [
            stem for stem in AVAILABLE_STEMS
            if stem not in instruments_to_remove
        ]

        if not stems_to_include:
            raise MixingError("Cannot remove all stems - at least one must remain")

        # Read and mix the stems
        mixed_audio = None
        sample_rate = None

        for stem_name in stems_to_include:
            stem_path = stems_dir / f"{stem_name}.wav"

            if not stem_path.exists():
                raise MixingError(f"Stem file not found: {stem_path}")

            # Read the stem audio
            audio, sr = sf.read(str(stem_path), dtype='float32')

            if sample_rate is None:
                sample_rate = sr
                mixed_audio = audio
            else:
                if sr != sample_rate:
                    raise MixingError(f"Sample rate mismatch: {sr} vs {sample_rate}")
                # Simple addition for mixing
                mixed_audio = mixed_audio + audio

        if mixed_audio is None:
            raise MixingError("No audio data to mix")

        # Normalize to prevent clipping
        max_amplitude = np.abs(mixed_audio).max()
        if max_amplitude > 0:
            mixed_audio = mixed_audio * (NORMALIZATION_HEADROOM / max_amplitude)

        # Generate output filename
        safe_title = _sanitize_filename(title)
        instruments_suffix = "_".join(instruments_to_remove)
        output_filename = f"{safe_title}_no_{instruments_suffix}.wav"
        output_path = output_dir / output_filename

        # Save the mixed audio as 32-bit float WAV (maximum quality)
        sf.write(
            str(output_path),
            mixed_audio,
            sample_rate,
            subtype='FLOAT'
        )

        return output_path

    except MixingError:
        raise
    except Exception as e:
        raise MixingError(f"Failed to mix stems: {str(e)}") from e


def _sanitize_filename(filename: str) -> str:
    """
    Remove special characters from filename to make it filesystem-safe.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')

    # Remove special characters, keep only alphanumeric, underscore, hyphen
    filename = re.sub(r'[^a-zA-Z0-9_\-]', '', filename)

    # Limit length to 100 characters
    if len(filename) > 100:
        filename = filename[:100]

    return filename or "output"

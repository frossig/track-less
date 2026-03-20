"""YouTube audio downloader using yt-dlp."""

from pathlib import Path
import yt_dlp

from .exceptions import DownloadError


def download_audio(url: str, output_dir: str, preview: bool = False) -> tuple[Path, str]:
    """
    Download audio from YouTube URL.

    Args:
        url: YouTube or YouTube Music URL
        output_dir: Directory to save the downloaded audio

    Returns:
        Tuple of (audio_file_path, video_title)

    Raises:
        DownloadError: If download fails
    """
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_dir_path / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',  # Original quality
        }],
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True,  # Only download the single track, not the full playlist
    }

    if preview:
        ydl_opts['download_ranges'] = yt_dlp.utils.download_range_func(None, [(0, 30)])
        ydl_opts['force_keyframes_at_cuts'] = True

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download and extract info in a single request
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise DownloadError(f"Could not extract information from URL: {url}")

            title = info.get('title', 'unknown')

            # Find the downloaded file
            audio_file = output_dir_path / f"{title}.wav"

            if not audio_file.exists():
                raise DownloadError(f"Downloaded file not found: {audio_file}")

            return audio_file, title

    except yt_dlp.utils.DownloadError as e:
        raise DownloadError(f"Failed to download audio: {str(e)}") from e
    except Exception as e:
        raise DownloadError(f"Unexpected error during download: {str(e)}") from e

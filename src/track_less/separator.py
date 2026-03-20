"""Stem separation using Demucs."""

from pathlib import Path
import torch
import torchaudio
import demucs.api

from .config import DEMUCS_MODEL
from .exceptions import SeparationError


def separate_stems(audio_file: Path, output_dir: str) -> Path:
    """
    Separate audio into individual stems using Demucs.

    Args:
        audio_file: Path to the audio file to separate
        output_dir: Directory to save the separated stems

    Returns:
        Path to the directory containing separated stems

    Raises:
        SeparationError: If separation fails
    """
    output_dir_path = Path(output_dir)
    stems_dir = output_dir_path / "stems"
    stems_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Initialize the Demucs separator with htdemucs_6s model
        # This model separates: drums, bass, vocals, guitar, piano, other
        separator = demucs.api.Separator(model=DEMUCS_MODEL, progress=True)

        # Separate the audio file
        origin, separated = separator.separate_audio_file(str(audio_file))

        # Save each stem as a WAV file
        for stem_name, source in separated.items():
            output_path = stems_dir / f"{stem_name}.wav"

            # Convert tensor to proper format and save using torchaudio
            # source is a tensor with shape (channels, samples)
            torchaudio.save(
                str(output_path),
                source.cpu(),
                separator.samplerate,
                encoding="PCM_F",  # 32-bit float
                bits_per_sample=32
            )

        return stems_dir

    except Exception as e:
        raise SeparationError(f"Failed to separate stems: {str(e)}") from e

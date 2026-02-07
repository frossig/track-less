"""Configuration constants for track-less."""

from pathlib import Path

# Output directory for processed audio files
OUTPUT_DIR = Path.home() / "Projects" / "track-less-output"

# Demucs model to use (6-stem separation including guitar)
DEMUCS_MODEL = "htdemucs_6s"

# Available stems from htdemucs_6s model
AVAILABLE_STEMS = ['drums', 'bass', 'vocals', 'guitar', 'piano', 'other']

# Normalization headroom (0.95 = 95% of max to prevent clipping)
NORMALIZATION_HEADROOM = 0.95

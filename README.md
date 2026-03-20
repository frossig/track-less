# track-less

A CLI tool to remove instrument tracks from songs using AI stem separation.

## Overview

`track-less` automates the process of removing specific instruments from songs:
1. Downloads audio from **YouTube, Spotify, Vimeo, SoundCloud** and 1800+ other sites (via [yt-dlp](https://github.com/yt-dlp/yt-dlp))
2. Uses [Demucs](https://github.com/facebookresearch/demucs) AI (htdemucs_6s model) to separate the song into 6 stems: drums, bass, vocals, guitar, piano, and other
3. Mixes the stems back together, excluding the instruments you specify
4. Outputs high-quality WAV files ready for playback

Perfect for musicians who want to practice along with songs minus their instrument!

## Features

- **Universal Download**: Works with YouTube, Spotify, Vimeo, SoundCloud, and 1800+ sites via [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **AI-Powered Separation**: Uses [Demucs](https://github.com/facebookresearch/demucs) htdemucs_6s for high-quality 6-stem separation
- **Simple CLI**: One command to download, separate, and mix
- **Guitar-Specific Removal**: Separates guitar as its own track (not lumped into "other")
- **High Quality Output**: 32-bit float WAV files with proper normalization
- **Automatic Cleanup**: Temporary files are removed automatically
- **Multiple Instrument Removal**: Remove any combination of: guitar, vocals, drums, bass, piano, or other
- **Stem Extraction**: Export raw stem files instead of remixing (great for DAW work)
- **Preview Mode**: Process only the first 30 seconds for quick testing

## Prerequisites

- Python 3.10 or higher
- ffmpeg (required by yt-dlp)

### Install ffmpeg

**macOS** (using Homebrew):
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows** (using Chocolatey):
```bash
choco install ffmpeg
```

## Installation

Install using pipx (recommended for CLI tools):

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install track-less
pipx install ~/Projects/track-less
```

Or install in editable mode for development:

```bash
pipx install --editable ~/Projects/track-less
```

Verify installation:

```bash
track-less --version
```

## Usage

### Basic Usage

Remove guitar from any supported site:

```bash
# YouTube
track-less "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -g

# SoundCloud
track-less "https://soundcloud.com/artist/track" -g

# Vimeo
track-less "https://vimeo.com/123456789" -g

# Spotify (requires Spotify Premium)
track-less "https://open.spotify.com/track/..." -g
```

Remove multiple instruments:

```bash
track-less "URL" -g -v  # Remove guitar and vocals
```

### Options

```
Usage: track-less [OPTIONS] URL

  Remove instrument tracks from songs using AI stem separation.

Arguments:
  URL  URL from YouTube, Spotify, Vimeo, SoundCloud, or any yt-dlp supported site

Options:
  -g, --guitar     Remove guitar track
  -v, --vocals     Remove vocals track
  -d, --drums      Remove drums track
  -b, --bass       Remove bass track
  -p, --piano      Remove piano track
  --other          Remove other instruments track
  -s, --stem       Extract stems instead of mixing (saves raw stem files)
  -P, --preview    Process only the first 30 seconds (quick test)
  -o, --output     Output directory (default: ~/Music/track-less)
  --version        Show the version and exit
  --help           Show this message and exit
```

### Examples

Remove guitar only:
```bash
track-less "URL" -g
```

Remove vocals and guitar (karaoke instrumental):
```bash
track-less "URL" -v -g
```

Remove drums (for drum practice):
```bash
track-less "URL" -d
```

Extract raw stem files (for DAW editing):
```bash
track-less "URL" -g -s        # saves guitar.wav separately
track-less "URL" -g -v -s     # saves guitar.wav and vocals.wav
```

Preview mode (only 30 seconds, much faster):
```bash
track-less "URL" -g -P
track-less "URL" -g -v -s -P  # combine with stem extraction
```

Custom output directory:
```bash
track-less "URL" -g -o ~/Music/practice-tracks
```

Works with any supported site:
```bash
track-less "https://soundcloud.com/artist/song" -b  # Remove bass
track-less "https://vimeo.com/123456" -v            # Remove vocals
```

### Supported Sites

**Popular sites that work:**
- ✅ **YouTube / YouTube Music** - No login required
- ✅ **SoundCloud** - Public tracks
- ✅ **Vimeo** - Public videos
- ✅ **Bandcamp** - Streamable tracks
- ✅ **Spotify** - ⚠️ Requires Spotify Premium account
- ✅ **1800+ other sites** - See [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

**Note**: Some platforms may require authentication or have restrictions on downloading.

## Output

- Default output directory: `~/Music/track-less/`
- Output format: 32-bit float WAV
- Filename format:
  - Normal mode: `{SongTitle}_no_{instruments}.wav` (e.g. `Song_no_guitar.wav`)
  - Stem mode (`-s`): `{SongTitle}_{instrument}.wav` (e.g. `Song_guitar.wav`)

## Performance

- **Download**: 30 seconds - 2 minutes (depends on network)
- **Separation**: 3-10 minutes (depends on CPU, GPU accelerates if available)
- **Mixing**: < 5 seconds
- **Total**: ~5-15 minutes per song

### First Run

The first time you run `track-less`, it will download the htdemucs_6s model (~2GB) to `~/.cache/demucs/`. This is a one-time download.

## System Requirements

- **RAM**: ~4GB (for Demucs processing)
- **Disk Space**:
  - ~2GB (model cache, one-time)
  - ~500MB per song (temporary files, auto-cleaned)
- **CPU**: Multi-core recommended (separation is CPU-intensive)
- **GPU**: Optional (CUDA-compatible GPU will accelerate separation)

## Troubleshooting

### "command not found: track-less"

Make sure pipx's bin directory is in your PATH:
```bash
python3 -m pipx ensurepath
# Then restart your terminal
```

### "ffmpeg not found"

Install ffmpeg using your package manager (see Prerequisites section above).

### Out of Memory

If you encounter memory errors during separation, close other applications to free up RAM. The htdemucs_6s model requires ~4GB of RAM.

### Slow Processing

Separation is CPU-intensive and can take 5-15 minutes per song. If you have a CUDA-compatible GPU, PyTorch will automatically use it to accelerate processing.

## Limitations

1. **Processing Time**: Separation takes several minutes per song (AI processing is intensive)
2. **Separation Quality**: Very good but not perfect - may leave some artifacts or affect similar-sounding instruments
3. **Source Quality**: Limited by the source's audio quality (varies by platform - typically 128-320kbps)
4. **GPU**: Currently auto-detects GPU but doesn't offer manual CPU/GPU selection

## Future Enhancements

See [ROADMAP.md](ROADMAP.md) for planned features including:
- Batch processing (multiple URLs)
- GPU acceleration detection and control
- Output format options (MP3, FLAC)
- Quality presets (fast/balanced/best)
- And many more!

## Development

### Setup Development Environment

```bash
# Clone/navigate to the project
cd ~/Projects/track-less

# Install in editable mode
pipx install --editable .

# Make changes to the code
# Changes will be reflected immediately when you run track-less
```

### Project Structure

```
track-less/
├── pyproject.toml              # Package configuration
├── README.md                   # User documentation (you are here)
├── QUICKSTART.md               # Quick start guide
├── ROADMAP.md                  # Future enhancements and feature ideas
├── INSTALLATION_NOTES.md       # Technical installation details
├── .gitignore                  # Git ignore patterns
└── src/
    └── track_less/
        ├── __init__.py         # Package version
        ├── cli.py              # CLI interface (Click)
        ├── downloader.py       # Media download (yt-dlp)
        ├── separator.py        # Stem separation (Demucs)
        ├── mixer.py            # Audio mixing (NumPy + soundfile)
        ├── config.py           # Configuration constants
        └── exceptions.py       # Custom exceptions
```

## License

This project is open source and available for educational and personal use.

## Credits

- **[Demucs](https://github.com/facebookresearch/demucs)**: AI stem separation by Meta Research
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: Universal media downloader supporting 1800+ sites

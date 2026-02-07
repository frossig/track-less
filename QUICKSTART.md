# Quick Start Guide

## Installation Complete! ✅

Your `track-less` CLI tool is installed and ready to use.

## Quick Test

Try it with any song from YouTube, Spotify, SoundCloud, Vimeo, or 1800+ other sites:

```bash
# Remove guitar from a song
track-less "URL_HERE" -g
```

## What Happens

1. **Downloads** the audio from the URL (30s-2min)
2. **Separates** into 6 stems using AI (3-10min)
   - First run downloads the model (~2GB, one-time)
3. **Mixes** stems without guitar (<5s)
4. **Saves** to `~/Projects/track-less-output/`

## Common Commands

```bash
# Remove guitar only
track-less "URL" -g

# Remove guitar and vocals (instrumental)
track-less "URL" -g -v

# Remove drums (for drum practice)
track-less "URL" -d

# Remove bass (for bass practice)
track-less "URL" -b

# Custom output directory
track-less "URL" -g -o ~/Music/practice
```

## Available Instruments

- `-g` / `--guitar` - Guitar track
- `-v` / `--vocals` - Vocals track
- `-d` / `--drums` - Drums track
- `-b` / `--bass` - Bass track
- `-p` / `--piano` - Piano track
- `--other` - Other instruments

## Output Format

- **Format**: 32-bit float WAV (maximum quality)
- **Location**: `~/Projects/track-less-output/`
- **Filename**: `{SongName}_no_{instrument}.wav`

Example: `Never_Gonna_Give_You_Up_no_guitar.wav`

## Tips

1. **First Run**: Will download the AI model (~2GB) - be patient!
2. **Processing Time**: 5-15 minutes per song is normal
3. **Quality**: Source is limited by the platform's audio quality (varies by site)
4. **Cleanup**: Temporary files are auto-deleted after processing
5. **Supported Sites**: YouTube, Spotify, Vimeo, SoundCloud, Bandcamp, and 1800+ more

## Troubleshooting

### "command not found: track-less"
```bash
# Ensure pipx is in your PATH
python3 -m pipx ensurepath
# Restart your terminal
```

### "ffmpeg not found"
```bash
# Install ffmpeg (macOS)
brew install ffmpeg
```

### Out of memory
- Close other applications
- The AI model needs ~4GB RAM

## Get Help

```bash
track-less --help     # Show all options
track-less --version  # Show version
```

## Example Session

```bash
$ track-less "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -g

track-less v0.1.0
Removing: guitar
Output directory: /Users/fausto/Projects/track-less-output

Step 1/3: Downloading audio from YouTube...
✓ Downloaded: Never Gonna Give You Up

Step 2/3: Separating stems with Demucs (this may take several minutes)...
Note: First run will download the htdemucs_6s model (~2GB)
✓ Separated into 6 stems

Step 3/3: Mixing stems...
✓ Mixed successfully

============================================================
Success! Output saved to:
  /Users/fausto/Projects/track-less-output/Never_Gonna_Give_You_Up_no_guitar.wav
============================================================
```

Enjoy your practice sessions! 🎸

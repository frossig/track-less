# track-less Roadmap

## Current Version: 0.1.0 ✅

The initial implementation is complete with core functionality:
- Single URL processing
- YouTube/YouTube Music download
- 6-stem separation (drums, bass, vocals, guitar, piano, other)
- High-quality WAV output
- Automatic cleanup

## Future Enhancements

### High Priority

#### 1. Progress Bars
**Status**: Not implemented
**Description**: Add visual progress indicators for each stage
- Download progress (percentage, speed)
- Separation progress (Demucs provides callbacks)
- Overall progress tracker

**Implementation**:
- Use `tqdm` library (already a demucs dependency)
- Add progress callbacks to downloader and separator
- Show estimated time remaining

```python
# Example
from tqdm import tqdm
# Progress bar for download
# Progress bar for each stem separation step
```

#### 2. Batch Processing
**Status**: Not implemented
**Description**: Process multiple URLs in one command
- Accept multiple URLs as arguments or from a file
- Process sequentially or in parallel (with --parallel flag)
- Summary report at the end

**Usage**:
```bash
# Multiple URLs
track-less -g URL1 URL2 URL3

# From file
track-less -g --from-file urls.txt

# Parallel processing (use multiple CPU cores)
track-less -g --parallel URL1 URL2 URL3
```

#### 3. Preview Mode
**Status**: Not implemented
**Description**: Process only first 30 seconds for quick testing
- Useful for testing if separation works well before full processing
- Much faster (~1-2 minutes vs 5-15 minutes)
- Saves bandwidth and time

**Usage**:
```bash
track-less -g --preview URL
# or
track-less -g --duration 30 URL
```

### Medium Priority

#### 4. GPU Acceleration Detection
**Status**: Partial (PyTorch auto-detects GPU)
**Description**: Better GPU detection and user feedback
- Detect if CUDA/MPS is available
- Show GPU status on startup
- Option to force CPU mode
- Estimate processing time based on hardware

**Usage**:
```bash
track-less -g --cpu URL  # Force CPU mode
track-less --show-device  # Show available compute device
```

#### 5. Output Format Options
**Status**: WAV only
**Description**: Support multiple output formats
- **MP3**: Smaller files, good for sharing (requires lameenc fix or ffmpeg)
- **FLAC**: Lossless compression, smaller than WAV
- **OGG**: Open format, good compression

**Note**: Currently blocked by lameenc on ARM64. Could use ffmpeg as alternative.

**Usage**:
```bash
track-less -g --format flac URL
track-less -g --format mp3 --bitrate 320 URL
```

#### 6. Quality Presets
**Status**: Not implemented
**Description**: Trade-off between speed and quality
- **fast**: Lower quality model, faster processing (~2-3 min)
- **balanced**: Current htdemucs_6s model (~5-15 min)
- **best**: Highest quality model, slower (~15-30 min)

**Usage**:
```bash
track-less -g --quality fast URL
track-less -g --quality best URL
```

**Models**:
- Fast: `htdemucs` (4-stem, faster)
- Balanced: `htdemucs_6s` (current, 6-stem)
- Best: `htdemucs_ft` (fine-tuned, highest quality)

### Low Priority

#### 7. Interactive Mode
**Status**: Not implemented
**Description**: Interactive CLI for selecting instruments
- Run without flags to enter interactive mode
- Select instruments with checkboxes
- Preview before processing

**Usage**:
```bash
track-less URL
# Shows interactive menu:
# ☑ Guitar
# ☐ Vocals
# ☐ Drums
# ☐ Bass
# ☐ Piano
# ☐ Other
```

#### 8. Stem Export
**Status**: Not implemented
**Description**: Save individual stems instead of mixing
- Useful for further editing in DAW
- Export all stems or selected ones
- Organized folder structure

**Usage**:
```bash
track-less --export-stems URL
# Creates: SongName/drums.wav, SongName/bass.wav, etc.

track-less --export-stems=guitar,vocals URL
# Only exports guitar and vocals stems
```

#### 9. Web Interface
**Status**: Not implemented
**Description**: Simple web UI for non-CLI users
- Drag-and-drop YouTube URL
- Select instruments with checkboxes
- Download button
- Progress visualization

**Tech Stack**:
- FastAPI or Flask backend
- Simple HTML/CSS/JS frontend
- Run locally with `track-less --web`

#### 10. Config File Support
**Status**: Not implemented
**Description**: Save preferences in config file
- Default output directory
- Default quality preset
- Default instruments to remove
- Favorite URLs/playlists

**Location**: `~/.track-less/config.yaml`

**Example**:
```yaml
output_dir: ~/Music/practice-tracks
quality: balanced
default_remove: [guitar]
notification: true
```

#### 11. Playlist Support
**Status**: Not implemented
**Description**: Process entire YouTube playlists
- Download all videos from playlist
- Batch process with progress
- Skip already processed songs

**Usage**:
```bash
track-less -g --playlist "PLAYLIST_URL"
```

#### 12. Audio Metadata
**Status**: Not implemented
**Description**: Preserve and add metadata to output files
- Copy original title, artist, album
- Add tags indicating removed instruments
- Embed album art

### Technical Debt / Improvements

#### Testing
- Add unit tests for each module
- Integration tests for full pipeline
- Mock yt-dlp and demucs for faster tests
- CI/CD pipeline

#### Error Handling
- Better error messages for network issues
- Retry logic for downloads
- Graceful degradation if GPU fails
- Recovery from interrupted processing

#### Performance
- Cache downloaded audio for re-processing
- Parallel stem processing (if possible)
- Optimize mixing algorithm
- Memory usage optimization for long songs

#### Documentation
- API documentation
- Architecture diagrams
- Contributing guide
- Video tutorials

## Community Requested Features

_This section will be populated based on user feedback and requests._

---

## How to Contribute

If you'd like to implement any of these features:

1. Fork the repository
2. Create a feature branch
3. Implement the feature with tests
4. Update documentation
5. Submit a pull request

## Notes

- Features marked as "Not implemented" are ideas for future versions
- Priority levels are suggestions and can change based on user needs
- Some features (like MP3 output) have technical blockers that need to be resolved first

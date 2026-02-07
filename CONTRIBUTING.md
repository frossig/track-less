# Contributing to track-less

First off, thank you for considering contributing to track-less! 🎸

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **System information** (OS, Python version, `track-less --version`)
- **Error messages** (full stack trace if available)

### Suggesting Enhancements

Check [ROADMAP.md](ROADMAP.md) first to see if your idea is already planned. For new suggestions:

- **Use a clear and descriptive title**
- **Detailed description** of the proposed feature
- **Use cases** - why would this be useful?
- **Possible implementation** (optional)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Update documentation** if needed
6. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
7. **Push to your fork** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/track-less.git
cd track-less

# Install in editable mode
pipx install --editable .

# Make changes and test
track-less "TEST_URL" -g

# Your changes are immediately reflected
```

## Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings for public functions
- Keep functions focused and small
- Comment complex logic

## Testing

Before submitting a PR:

```bash
# Test basic functionality
track-less --version
track-less --help

# Test with a short YouTube video (1-2 min)
track-less "SHORT_VIDEO_URL" -g

# Verify output quality
```

## Project Structure

```
src/track_less/
├── cli.py          # CLI interface - Click commands
├── downloader.py   # YouTube download logic
├── separator.py    # Demucs stem separation
├── mixer.py        # Audio mixing and normalization
├── config.py       # Configuration constants
└── exceptions.py   # Custom exception classes
```

## Areas We'd Love Help With

See [ROADMAP.md](ROADMAP.md) for planned features:

**High Priority:**
- Progress bars for download/separation
- Batch processing (multiple URLs)
- Preview mode (first 30 seconds)
- GPU detection and control

**Medium Priority:**
- Output format options (MP3, FLAC)
- Quality presets (fast/balanced/best)
- Better error messages

**Other:**
- Unit tests
- CI/CD pipeline
- Documentation improvements
- Bug fixes

## Questions?

Feel free to open an issue with the `question` label.

## Code of Conduct

- Be respectful and inclusive
- Constructive criticism is welcome
- Focus on what is best for the community
- Show empathy towards other community members

Thank you for contributing! 🎵

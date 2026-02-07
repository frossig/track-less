"""Custom exceptions for track-less."""


class TrackLessError(Exception):
    """Base exception for all track-less errors."""
    pass


class DownloadError(TrackLessError):
    """Error during audio download from YouTube."""
    pass


class SeparationError(TrackLessError):
    """Error during stem separation with Demucs."""
    pass


class MixingError(TrackLessError):
    """Error during audio mixing."""
    pass

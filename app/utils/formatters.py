"""Formatters for converting bytes, time, and creating progress bars."""

import math
from datetime import datetime


def format_date(dt: datetime | None) -> str:
    """Convert datetime into human-readable date string."""
    if not dt:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M")


def format_size(byte: int | float) -> str:
    """Convert bytes into human-readable size.

    Args:
        byte: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 GB")
    """
    if byte == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(byte, 1024)))
    p = math.pow(1024, i)
    s = round(byte / p, 2)
    return f"{s} {size_name[i]}"


def format_time(seconds: int | float) -> str:
    """Convert seconds into human-readable time.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string (e.g., "1.5 Hrs")
    """
    if seconds == 0:
        return "0 Sec"

    size_name = ("Sec", "Min", "Hrs")
    i = int(math.floor(math.log(seconds, 60)))
    p = math.pow(60, i)
    s = round(seconds / p, 2)
    return f"{s} {size_name[i]}"


def progress_bar(progress: float | int, length: int = 20) -> str:
    """Create a progress bar visualization.

    Args:
        progress: Progress percentage (0-100)
        length: Length of the progress bar (default: 20)

    Returns:
        Progress bar string with filled and empty blocks
    """
    bars = int(float(progress)) // (100 // length)
    filled = "\u25a3"  # ▣
    empty = "\u25a2"  # ▢
    return f"{filled * bars}{empty * (length - bars)}"


def space_bar(total_space: int | float, space_used: int | float, length: int = 20) -> str:
    """Create a storage space usage bar.

    Args:
        total_space: Total available space in bytes
        space_used: Used space in bytes
        length: Length of the bar (default: 20)

    Returns:
        Space usage bar string
    """
    filled = "\u25a3"  # ▣
    empty = "\u25a2"  # ▢

    if total_space == 0:
        return empty * length

    bars = round((space_used / total_space) * length)
    return f"{filled * bars}{empty * (length - bars)}"

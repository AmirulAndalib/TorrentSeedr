"""Utility functions for formatting text, sizes, dates, and times."""

import math
from datetime import datetime

from app.utils.language import Translator


def format_date(dt: datetime | None) -> str:
    """Convert datetime into human-readable date string."""
    if not dt:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M")


def format_size(byte: int | float) -> str:
    """Convert bytes into human-readable size."""
    if byte == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(byte, 1024)))
    p = math.pow(1024, i)
    s = round(byte / p, 2)
    return f"{s} {size_name[i]}"


def format_time(seconds: int | float) -> str:
    """Convert seconds into human-readable time."""
    if seconds == 0:
        return "0 Sec"

    size_name = ("Sec", "Min", "Hrs")
    i = int(math.floor(math.log(seconds, 60)))
    p = math.pow(60, i)
    s = round(seconds / p, 2)
    return f"{s} {size_name[i]}"


def progress_bar(progress: float | int, translator: Translator, length: int = 20) -> str:
    """Create a progress bar visualization."""
    bars = int(float(progress)) // (100 // length)
    filled = translator.get("progressBarFilledEmoji")
    empty = translator.get("progressBarEmptyEmoji")
    return f"{filled * bars}{empty * (length - bars)}"

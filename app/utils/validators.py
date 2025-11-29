import re


def extract_magnet_from_text(text: str) -> str | None:
    """Extract magnet link from text.

    Args:
        text: Text containing potential magnet link

    Returns:
        Magnet link if found, None otherwise
    """
    pattern = r"magnet:\?[^\s]+"
    match = re.search(pattern, text)
    return match.group(0) if match else None

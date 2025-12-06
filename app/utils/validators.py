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


def parse_callback_data(data: str) -> dict:
    """
    Parses a callback string into a dictionary of key-value pairs.
    The string is expected to be in a consistent "{key}_{value}_{key}_{value}..." format.

    Example: "folder_123_page_2_parent_456" -> {'folder': '123', 'page': '2', 'parent': '456'}
    """
    parts = data.split("_")
    # Take elements at even positions as keys and odd positions as values.
    return dict(zip(parts[0::2], parts[1::2]))

"""Views package for the bot."""

from typing import NamedTuple

from telethon.tl.types import TypeKeyboardButton


class ViewResponse(NamedTuple):
    """A standard response from a view function."""

    message: str
    buttons: list[list[TypeKeyboardButton]] | None = None

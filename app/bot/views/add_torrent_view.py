"""Views for adding torrents."""

from textwrap import dedent

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_add_torrent_success(translator: Translator, torrent_title: str | None = "") -> ViewResponse:
    """Render the success message after adding a torrent."""
    message = dedent(f"""
        {translator.get("downloadAddedSuccessfully")}

        <b>{torrent_title}</b>
    """)
    return ViewResponse(message=message.strip())


def render_item_already_in_queue(translator: Translator) -> ViewResponse:
    """Render the message when item is already in the download queue."""
    message = translator.get("downloadAlreadyInQueue")
    return ViewResponse(message=message)


def render_queue_full_added_to_wishlist(translator: Translator) -> ViewResponse:
    """Render the message when queue is full and the item is added to wishlist."""
    message = translator.get("downloadAddedToWishlist")
    buttons = [Button.url(translator.get("upgradeToPremiumBtn"), "https://www.seedr.cc/subscription")]

    return ViewResponse(message=message, buttons=buttons)


def render_not_enough_space_added_to_wishlist(translator: Translator) -> ViewResponse:
    """Render the message when there is not enough space and the item is added to wishlist."""
    message = translator.get("notEnoughSpaceAddedToWishlist")

    buttons = [Button.url(translator.get("upgradeToPremiumBtn"), "https://www.seedr.cc/subscription")]
    return ViewResponse(message=message, buttons=buttons)


def render_invalid_magnet_message(translator: Translator) -> ViewResponse:
    """Render the message for an invalid magnet link."""
    return ViewResponse(message=translator.get("invalidMagnet"))


def render_file_too_large_message(max_size: str, translator: Translator) -> ViewResponse:
    """Render the message for a file that is too large."""
    message = translator.get("fileTooLarge").format(max_size=max_size)
    return ViewResponse(message=message)

"""Views for add torrent messages."""

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_add_torrent_success(torrent_title: str, translator: Translator) -> ViewResponse:
    """Render the success message after adding a torrent."""
    message = f"{translator.get('torrentAddedSuccessfully')}\n\n<b>{torrent_title}</b>"
    return ViewResponse(message=message)


def render_add_torrent_failure(translator: Translator) -> ViewResponse:
    """Render the failure message after adding a torrent."""
    message = translator.get("somethingWrong")
    return ViewResponse(message=message)


def render_torrent_file_upload_not_supported(translator: Translator) -> ViewResponse:
    """Render message for unsupported torrent file upload."""
    message = translator.get("torrentFileUploadNotSupported")
    return ViewResponse(message=message)


def render_invalid_magnet_message(translator: Translator) -> ViewResponse:
    """Render the message for an invalid magnet link."""
    return ViewResponse(message=translator.get("invalidMagnet"))


def render_file_too_large_message(max_size: str, translator: Translator) -> ViewResponse:
    """Render the message for a file that is too large."""
    message = translator.get("fileTooLarge").format(max_size=max_size)
    return ViewResponse(message=message)

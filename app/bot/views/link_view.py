"""Views for displaying download links."""

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_file_link_message(file_result, translator: Translator) -> ViewResponse:
    """Render the file download link message."""
    message = (
        f"<b>{translator.get('fileEmoji')} {file_result.name}</b>\n\n"
        f"<b>{translator.get('downloadLinkLabel')}</b>:\n"
        f"<code>{file_result.url}</code>"
    )
    buttons = [[Button.url(translator.get("downloadFileBtn"), file_result.url)]]
    return ViewResponse(message=message, buttons=buttons)


def render_folder_link_message(archive_url: str, translator: Translator) -> ViewResponse:
    """Render the folder download link message."""
    message = (
        f"<b>{translator.get('folderEmoji')} {translator.get('folderDownloadLinkLabel')}</b>\n\n"
        f"<b>{translator.get('downloadLinkLabel')}</b>:\n"
        f"<code>{archive_url}</code>"
    )
    buttons = [[Button.url(translator.get("downloadFolderBtn"), archive_url)]]
    return ViewResponse(message=message, buttons=buttons)

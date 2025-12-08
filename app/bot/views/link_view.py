from textwrap import dedent

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_file_link_message(file_result, translator: Translator) -> ViewResponse:
    """Render the file download link message."""
    message = dedent(f"""
        <b>{translator.get('fileEmoji')} {file_result.name}</b>

        <b>{translator.get('downloadLinkLabel')}</b>:
        <code>{file_result.url}</code>
    """)
    buttons = [[Button.url(translator.get("downloadFileBtn"), file_result.url)]]
    return ViewResponse(message=message.strip(), buttons=buttons)


def render_folder_link_message(archive_url: str, translator: Translator) -> ViewResponse:
    """Render the folder download link message."""
    message = dedent(f"""
        <b>{translator.get('folderEmoji')} {translator.get('folderDownloadLinkLabel')}</b>

        <b>{translator.get('downloadLinkLabel')}</b>:
        <code>{archive_url}</code>
    """)
    buttons = [[Button.url(translator.get("downloadFolderBtn"), archive_url)]]
    return ViewResponse(message=message.strip(), buttons=buttons)

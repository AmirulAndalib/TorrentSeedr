"""Views for active downloads."""
from textwrap import dedent

from telethon import Button

from app.bot.views import ViewResponse
from app.utils import format_size, progress_bar
from app.utils.language import Translator


def render_download_status(download, translator: Translator) -> ViewResponse:
    """Renders the detailed progress message for a single download."""
    name = download.name
    progress = int(download.progress)
    size = download.size
    downloaded = (progress / 100) * size if size else 0
    progress_visual = progress_bar(progress)

    message = dedent(f"""
        <b>{translator.get('activeDownloadsBtn')}</b>

        <b>{name}</b>
           {progress_visual} {float(progress):.1f}%
           {translator.get('sizeLabel')}: {format_size(downloaded)} / {format_size(size)}
    """)
    if download.download_rate:
        speed = format_size(download.download_rate)
        message += f"\n   {translator.get('speedLabel')}: {speed}/s"

    buttons = [[Button.inline(translator.get("cancelBtn"), f"cancel_download_{download.id}".encode())]]
    return ViewResponse(message=message.strip(), buttons=buttons)


def render_download_menu(active_downloads, translator: Translator) -> ViewResponse:
    """Render a menu of buttons for multiple active downloads."""
    message = dedent(f"""
        <b>{translator.get('activeDownloadsBtn')}</b>

        {translator.get('selectDownload')}
    """)
    buttons = []
    for download in active_downloads:
        button_text = (
            f"{download.name[:30]}... ({int(download.progress)}%)"
            if len(download.name) > 30
            else f"{download.name} ({int(download.progress)}%)"
        )
        buttons.append([Button.inline(button_text, f"active_{download.id}".encode())])
    return ViewResponse(message=message.strip(), buttons=buttons)


def render_no_downloads_message(translator: Translator) -> ViewResponse:
    """Render the message when there are no active downloads."""
    return ViewResponse(message=translator.get("noActiveDownloads"))

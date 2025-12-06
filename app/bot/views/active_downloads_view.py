"""Views for active downloads."""

from app.bot.views import ViewResponse
from app.utils import format_size, format_time, progress_bar
from app.utils.language import Translator


def render_active_downloads_message(active_downloads, translator: Translator) -> ViewResponse:
    message = f"<b>{translator.get('activeDownloadsBtn')}</b>\n\n"
    for idx, torrent in enumerate(active_downloads, 1):
        name = torrent.name
        progress = torrent.progress
        size = torrent.size
        downloaded = (progress / 100) * size if size else 0
        progress_visual = progress_bar(progress)
        message += f"<b>{idx}. {name}</b>\n"
        message += f"   {progress_visual} {progress:.1f}%\n"
        message += f"   {translator.get('sizeLabel')}: {format_size(downloaded)} / {format_size(size)}\n"
        if torrent.download_rate:
            speed = format_size(torrent.download_rate)
            message += f"   {translator.get('speedLabel')}: {speed}/s\n"
        if torrent.eta:
            eta = format_time(torrent.eta)
            message += f"   {translator.get('etaLabel')}: {eta}\n"
        message += "\n"

    return ViewResponse(message=message)


def render_no_active_downloads_message(translator: Translator) -> ViewResponse:
    """Render the message when there are no active downloads."""
    return ViewResponse(message=translator.get("noActiveDownloads"))

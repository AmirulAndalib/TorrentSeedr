from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.add_torrent_view import (
    render_add_torrent_failure,
    render_add_torrent_success,
    render_file_too_large_message,
    render_wrong_torrent_file_message,
)
from app.bot.views.shared_view import render_processing_message
from app.config import settings
from app.database.models import User
from app.utils import extract_magnet_from_text, format_size
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def add_torrent_handler(
    event: events.NewMessage.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
    magnet_link: str | None = None,
    **kwargs,
):
    """Handle adding torrent from magnet link."""
    if not magnet_link:
        magnet_link = extract_magnet_from_text(event.message.text)

    view = render_processing_message(translator)
    status_message = await event.respond(view.message, buttons=view.buttons)

    result = await seedr_client.add_torrent(magnet_link)

    if result.title:
        view = render_add_torrent_success(result.title, translator)
        await status_message.edit(view.message, buttons=view.buttons)
    else:
        view = render_add_torrent_failure(translator)
        await status_message.edit(view.message, buttons=view.buttons)


@setup_handler(require_auth=True)
async def handle_torrent_file(
    event: events.NewMessage.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    """Handle torrent file upload."""
    if not event.message.document or not event.message.file.name.endswith(".torrent"):
        view = render_wrong_torrent_file_message(translator)
        await event.respond(view.message, buttons=view.buttons)
        return

    # Check file size before downloading
    if event.message.file.size > settings.max_torrent_file_size:
        max_size_mb = format_size(settings.max_torrent_file_size)
        view = render_file_too_large_message(max_size_mb, translator)
        await event.respond(view.message, buttons=view.buttons)
        return

    view = render_processing_message(translator)
    status_message = await event.respond(view.message, buttons=view.buttons)

    file_bytes = await event.message.download_media(bytes)
    result = await seedr_client.add_torrent(file_bytes)

    if result.title:
        view = render_add_torrent_success(result.title, translator)
        await status_message.edit(view.message, buttons=view.buttons)
    else:
        view = render_add_torrent_failure(translator)
        await status_message.edit(view.message, buttons=view.buttons)

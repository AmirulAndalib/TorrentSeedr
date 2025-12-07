"""Active command handler."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.active_downloads_view import (
    render_download_menu,
    render_download_status,
    render_no_downloads_message,
)
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def active_handler(
    event: events.NewMessage.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    contents = await seedr_client.list_contents()

    active_downloads = []
    if contents.torrents:
        active_downloads = [t for t in contents.torrents]

    if not active_downloads:
        view = render_no_downloads_message(translator)
        await event.respond(view.message, buttons=view.buttons)
        return

    # View based on number of downloads
    if len(active_downloads) > 1:
        view = render_download_menu(active_downloads, translator)
    else:
        view = render_download_status(active_downloads[0], translator)

    await event.respond(view.message, buttons=view.buttons)

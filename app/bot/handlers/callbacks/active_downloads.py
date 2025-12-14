"""Callback handlers for active downloads."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.active_downloads_view import render_download_status
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def active_download_callback(
    event: events.CallbackQuery.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    callback_data = event.data.decode()
    download_id = int(callback_data.replace("active_", ""))

    contents = await seedr_client.list_contents()

    active_download = next((t for t in contents.torrents if t.id == download_id), None)

    if active_download:
        view = render_download_status(active_download, translator)
        await event.edit(view.message, buttons=view.buttons)
        return

    await event.answer(translator.get("downloadNotFound"), alert=True)


@setup_handler(require_auth=True)
async def cancel_download_callback(
    event: events.CallbackQuery.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    """Handle cancelling an active download."""
    download_id = str(event.data.decode().replace("cancel_download_", ""))

    await seedr_client.delete_torrent(download_id)

    await event.edit(translator.get("downloadCancelled"))

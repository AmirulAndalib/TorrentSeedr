"""Download link generation callback handlers."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.files_view import (
    render_error_fetching_link_message,
    render_file_link_message,
    render_folder_link_message,
)
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def file_link_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """Handle file download link generation."""
    file_id = str(int(event.data.decode().replace("file_link_", "")))
    result = await seedr_client.fetch_file(file_id)
    if result.url:
        await event.answer(translator.get("fetchingLink"), alert=False)
        view = render_file_link_message(result, translator)
        await event.edit(view.message, buttons=view.buttons, link_preview=False)
    else:
        view = render_error_fetching_link_message(translator)
        await event.edit(view.message, buttons=view.buttons)


@setup_handler(require_auth=True)
async def folder_link_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """Handle folder download link generation."""
    folder_id = str(int(event.data.decode().replace("folder_link_", "")))
    result = await seedr_client.create_archive(folder_id)
    if result.archive_url:
        await event.answer(translator.get("fetchingLink"), alert=False)
        view = render_folder_link_message(result.archive_url, translator)
        await event.edit(view.message, buttons=view.buttons, link_preview=False)
    else:
        view = render_error_fetching_link_message(translator)
        await event.edit(view.message, buttons=view.buttons)

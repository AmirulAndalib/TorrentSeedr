"""File and folder deletion callback handlers."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.files_view import (
    render_failed_to_delete_file_message,
    render_failed_to_delete_folder_message,
)
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def delete_file_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """Handle file deletion callback."""
    file_id = str(int(event.data.decode().replace("delete_file_", "")))
    result = await seedr_client.delete_file(file_id)
    if result.result:
        await event.answer(translator.get("removedSuccessfully"), alert=False)
        await event.delete()
    else:
        view = render_failed_to_delete_file_message(translator)
        await event.edit(view.message, buttons=view.buttons)


@setup_handler(require_auth=True)
async def delete_folder_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """Handle folder deletion callback."""
    folder_id = str(int(event.data.decode().replace("delete_folder_", "")))
    result = await seedr_client.delete_folder(folder_id)
    if result.result:
        await event.answer(translator.get("deletedSuccessfully"), alert=False)
        await event.delete()
    else:
        view = render_failed_to_delete_folder_message(translator)
        await event.edit(view.message, buttons=view.buttons)

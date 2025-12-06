"""File and folder navigation callback handlers."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.files_view import (
    render_file_details_message,
    render_folder_contents_message,
)
from app.database.models import User
from app.utils.language import Translator
from app.utils.validators import parse_callback_data


@setup_handler(require_auth=True)
async def folder_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """
    Handle folder navigation callback.

    Callback data is a series of key-value pairs separated by underscores.
    Example: "folder_123_page_2_parent_456"
    """
    callback_data = event.data.decode()
    params = parse_callback_data(callback_data)

    folder_id = params.get("folder", "")
    page = int(params.get("page", 1))
    parent_id = params.get("parent")

    contents = await seedr_client.list_contents(folder_id=folder_id)
    view = render_folder_contents_message(contents, folder_id, parent_id, page, translator)
    await event.edit(view.message, buttons=view.buttons)


@setup_handler(require_auth=True)
async def file_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """
    Handle file view callback.

    Callback data is a series of key-value pairs separated by underscores.
    Example: "file_789_parent_123_type_video"
    """
    callback_data = event.data.decode()
    params = parse_callback_data(callback_data)

    file_id = params.get("file", "")
    parent_folder_id = params.get("parent")
    media_type = params.get("type")  # e.g., "video", "audio", or None

    is_video = media_type == "video"
    is_audio = media_type == "audio"

    if not parent_folder_id:
        await event.answer(translator.get("cannotDetermineFolder"), alert=True)
        return

    contents = await seedr_client.list_contents(folder_id=parent_folder_id)
    file_metadata = next((f for f in contents.files if str(f.folder_file_id) == file_id), None)

    if not file_metadata:
        await event.answer(translator.get("fileNotFound"), alert=True)
        return

    playlist_format = user.playlist_format or "m3u"
    view = render_file_details_message(
        file_metadata=file_metadata,
        is_video=is_video,
        is_audio=is_audio,
        file_id=file_id,
        parent_folder_id=parent_folder_id,
        playlist_format=playlist_format,
        translator=translator,
    )
    await event.edit(view.message, link_preview=False, buttons=view.buttons)

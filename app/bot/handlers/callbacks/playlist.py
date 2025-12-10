"""Playlist-related callback handlers."""

import os

from seedrcc import AsyncSeedr
from telethon import events
from telethon.tl import types

from app.bot.decorators import setup_handler
from app.bot.views.playlist_view import (
    render_playlist_message,
)
from app.database import get_session
from app.database.models import User
from app.database.repository import UserRepository
from app.utils.language import Translator
from app.utils.playlist import generate_file_playlist, generate_folder_playlist


@setup_handler(require_auth=True)
async def playlist_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """Handle playlist generation callback."""
    callback_data = event.data.decode()
    parts = callback_data.split("_")
    playlist_type = parts[1]
    media_type = parts[2]
    media_id_str = "_".join(parts[3:])

    async with get_session() as session:
        await UserRepository(session).update_settings(event, user.id, playlist_format=playlist_type)

    playlist_result = None
    if media_type == "file":
        playlist_result = await generate_file_playlist(seedr_client, media_id_str, playlist_type)
    else:  # Folder
        folder_id = media_id_str if media_id_str != "root" else "0"
        playlist_result = await generate_folder_playlist(seedr_client, folder_id, playlist_type)

    if playlist_result and os.path.exists(playlist_result.file_path):
        playlist_file, desired_filename = playlist_result

        # Select the local thumbnail file path
        thumbnail_file_path = f"images/{playlist_type}.jpg"

        try:
            view = render_playlist_message(playlist_type, media_type, media_id_str, translator)
            with open(playlist_file, "rb") as f, open(thumbnail_file_path, "rb") as thumbnail_f:
                await event.edit(
                    view.message,
                    file=f,
                    attributes=[types.DocumentAttributeFilename(file_name=desired_filename)],
                    thumb=thumbnail_f,
                    buttons=view.buttons,
                )
        finally:
            os.remove(playlist_file)
    else:
        await event.answer(translator.get("noPlayableMedia"), alert=True)

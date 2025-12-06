"""Playlist-related callback handlers."""

import os

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.playlist_view import (
    render_no_playable_media_message,
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
    await event.answer(translator.get("processing"), alert=False)

    callback_data = event.data.decode()
    parts = callback_data.split("_")
    playlist_type = parts[1]
    media_type = parts[2]
    media_id_str = "_".join(parts[3:])

    async with get_session() as session:
        await UserRepository(session).update_settings(user.id, playlist_format=playlist_type)

    playlist_file = None
    if media_type == "file":
        playlist_file = await generate_file_playlist(seedr_client, media_id_str, playlist_type)
    else:  # Folder
        folder_id = media_id_str if media_id_str != "root" else None
        playlist_file = await generate_folder_playlist(seedr_client, folder_id or "0", playlist_type)

    if playlist_file and os.path.exists(playlist_file):
        try:
            view = render_playlist_message(playlist_type, media_type, media_id_str, translator)
            with open(playlist_file, "rb") as f:
                await event.edit(view.message, file=f, buttons=view.buttons)
        finally:
            os.remove(playlist_file)
    else:
        view = render_no_playable_media_message(translator)
        await event.edit(view.message, buttons=view.buttons)


"""File browser handler."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.files_view import render_files_message, render_no_files_message
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def files_handler(
    event: events.NewMessage.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
    folder_id: str | None = None,
):
    contents = await seedr_client.list_contents(folder_id=folder_id or "0")
    folders = contents.folders

    if not folders:
        view = render_no_files_message(translator)
        await event.respond(view.message, buttons=view.buttons)
        return

    view = render_files_message(folders, translator)

    await event.respond(view.message, buttons=view.buttons)

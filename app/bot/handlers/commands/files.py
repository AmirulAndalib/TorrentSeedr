"""File browser handler."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.navigation_view import render_folder_contents_message
from app.bot.views.status_view import render_no_files_message
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

    if not contents.folders or contents.files:
        view = render_no_files_message(translator)
        await event.respond(view.message, buttons=view.buttons)
        return

    view = render_folder_contents_message(contents, folder_id="0", parent_id=None, page=1, translator=translator)

    await event.respond(view.message, buttons=view.buttons)

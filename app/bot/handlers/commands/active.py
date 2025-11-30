"""Active torrents handler."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.active_torrents_view import (
    render_active_torrents_message,
    render_no_active_torrents_message,
)
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def active_torrents_handler(
    event: events.NewMessage.Event | events.CallbackQuery.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    is_callback = isinstance(event, events.CallbackQuery.Event)

    contents = await seedr_client.list_contents()

    active_torrents = []
    if contents.torrents:
        active_torrents = [t for t in contents.torrents if int(t.progress) < 100]

    if not active_torrents:
        view = render_no_active_torrents_message(translator)
        if is_callback:
            await event.edit(view.message, buttons=view.buttons)
        else:
            await event.respond(view.message, buttons=view.buttons)
        return

    view = render_active_torrents_message(active_torrents, translator)

    if is_callback:
        await event.edit(view.message, buttons=view.buttons)
    else:
        await event.respond(view.message, buttons=view.buttons)

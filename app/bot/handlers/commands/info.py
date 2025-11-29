"""Account info handler."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.info_view import render_account_info
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def info_handler(
    event: events.NewMessage.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    settings = await seedr_client.get_settings()
    account_info = settings.account

    view = render_account_info(account_info, translator)

    await event.respond(view.message, buttons=view.buttons)

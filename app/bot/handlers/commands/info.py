"""Account info handler."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.info_view import render_account_info
from app.bot.views.shared_view import render_processing_message
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def info_handler(
    event: events.NewMessage.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    processing_view = render_processing_message(translator)
    status_message = await event.respond(processing_view.message)

    settings = await seedr_client.get_settings()
    account_info = settings.account

    view = render_account_info(account_info, translator)

    await status_message.edit(view.message, buttons=view.buttons)

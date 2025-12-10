"""Start command handler."""

from telethon import events

from app.bot.decorators import setup_handler
from app.bot.handlers.messages.add_torrent import add_torrent_handler
from app.bot.utils.commands import set_user_commands
from app.bot.views.start_view import render_start_message
from app.database.models import User
from app.utils.language import Translator


@setup_handler()
async def start_handler(event: events.NewMessage.Event, user: User, translator: Translator):
    has_accounts = bool(user.default_account_id)

    # Check for deep link start parameter
    if has_accounts and event.message.text.startswith("/start addTorrent_"):
        param = event.message.text.split()[1]
        torrent_hash = param.split("_")[-1]
        magnet_link = f"magnet:?xt=urn:btih:{torrent_hash}"

        await add_torrent_handler(event, magnet_link=magnet_link)
        raise events.StopPropagation()

    await set_user_commands(event, translator, has_accounts)

    view = render_start_message(
        has_accounts=has_accounts,
        translator=translator,
    )

    await event.respond(
        view.message,
        buttons=view.buttons,
    )

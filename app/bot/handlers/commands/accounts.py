"""Accounts management command handler."""

from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.accounts_view import render_accounts_message
from app.database import get_session
from app.database.models import User
from app.database.repository import AccountRepository
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def accounts_handler(
    event: events.NewMessage.Event | events.CallbackQuery.Event,
    user: User,
    translator: Translator,
):
    """Shows list of accounts and management options."""
    is_callback = isinstance(event, events.CallbackQuery.Event)

    async with get_session() as session:
        account_repo = AccountRepository(session)
        accounts = await account_repo.get_by_user_id(user.id)

    view = render_accounts_message(accounts, user.default_account_id, translator)

    if is_callback:
        await event.edit(view.message, buttons=view.buttons)
    else:
        await event.respond(view.message, buttons=view.buttons)

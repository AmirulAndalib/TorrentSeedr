"""Utility functions for handling conversations."""

from telethon import events
from telethon.tl.custom.conversation import Conversation

from app.bot.views import ViewResponse
from app.bot.views.login_view import render_cancelled_login_message
from app.utils.language import Translator


async def cancel_conversation(conv: Conversation, translator: Translator, has_accounts: bool):
    """Generic helper to cancel a conversation and show a message."""
    view = render_cancelled_login_message(translator=translator, has_accounts=has_accounts)
    await conv.send_message(view.message, buttons=view.buttons)
    conv.cancel()
    raise events.StopPropagation()


async def ask(
    conv: Conversation,
    view: ViewResponse,
    translator: Translator,
    has_accounts: bool,
    delete_input: bool = False,
) -> str:
    """
    Sends a prompt, gets a response, and handles cancellation automatically.

    Returns:
        The text of the user's response.
    """
    cancel_text = translator.get("cancelBtn")

    await conv.send_message(view.message, buttons=view.buttons)
    response_msg = await conv.get_response()
    response_text = response_msg.text.strip()
    if delete_input:
        await response_msg.delete()

    if response_text == cancel_text:
        await cancel_conversation(conv, translator, has_accounts)

    return response_text

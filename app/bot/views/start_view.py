"""Views for /start command."""

from app.bot.views import ViewResponse
from app.bot.views.shared_view import get_main_keyboard
from app.utils.language import Translator


def render_start_message(has_accounts: bool, translator: Translator) -> ViewResponse:
    if has_accounts:
        message = translator.get("greet")
    else:
        message = translator.get("welcomeMessage")

    keyboard = get_main_keyboard(has_accounts, translator)

    return ViewResponse(message=message, buttons=keyboard)

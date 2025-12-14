"""Views for login management."""

from telethon import Button

from app.bot.views import ViewResponse
from app.bot.views.shared_view import get_main_keyboard
from app.utils.language import Translator


def render_login_message(translator: Translator) -> ViewResponse:
    "Render view for /login"
    message = translator.get("loginMessage")
    buttons = [
        [
            Button.inline(
                translator.get("loginWithEmailBtn"),
                b"login_email",
            )
        ],
        [
            Button.inline(
                translator.get("authorizeWithDeviceBtn"),
                b"authorize_device",
            )
        ],
    ]
    return ViewResponse(message=message, buttons=buttons)


def render_enter_email(translator: Translator) -> ViewResponse:
    """Render the enter email message."""
    keyboard = [[Button.text(translator.get("cancelBtn"), resize=True)]]
    return ViewResponse(message=translator.get("enterEmail"), buttons=keyboard)


def render_enter_password_for(email: str, translator: Translator) -> ViewResponse:
    """Render the enter password for message."""
    message = translator.get("enterPasswordFor").format(email=email)
    keyboard = [[Button.text(translator.get("cancelBtn"), resize=True)]]
    return ViewResponse(message=message, buttons=keyboard)


def render_logging_in(translator: Translator) -> ViewResponse:
    """Render the logging in message."""
    return ViewResponse(message=translator.get("loggingIn"))


def render_logged_in(username: str, translator: Translator) -> ViewResponse:
    """Render the logged in message."""
    keyboard = get_main_keyboard(True, translator)
    message = translator.get("loggedInAs").format(username=username)
    return ViewResponse(message=message, buttons=keyboard)


def render_cancelled_login_message(translator: Translator, has_accounts: bool) -> ViewResponse:
    """Render the cancelled login message."""
    keyboard = get_main_keyboard(has_accounts, translator)
    message = translator.get("cancelled")
    return ViewResponse(message=message, buttons=keyboard)


def render_incorrect_password(translator: Translator, has_accounts: bool) -> ViewResponse:
    """Render the incorrect password message."""
    keyboard = get_main_keyboard(has_accounts, translator)
    return ViewResponse(message=translator.get("incorrectPassword"), buttons=keyboard)


def render_authorize_device(device_code: str, user_code: str, translator: Translator) -> ViewResponse:
    """Render the authorize device message."""
    buttons = [[Button.inline(translator.get("doneBtn"), f"auth_complete_{device_code}".encode())]]
    message = translator.get("authorize").format(code=user_code)
    return ViewResponse(message=message, buttons=buttons)


def render_auth_failed(error: str, translator: Translator) -> ViewResponse:
    """Render the auth failed message."""
    message = translator.get("authFailed").format(error=error)
    return ViewResponse(message=message)


def render_store_password_prompt(translator: Translator) -> ViewResponse:
    """Render the store password prompt."""
    message = translator.get("storePasswordPrompt")
    buttons = [
        [
            Button.text(translator.get("yesBtn"), resize=True),
            Button.text(translator.get("noBtn"), resize=True),
        ],
        [Button.text(translator.get("cancelBtn"), resize=True)],
    ]
    return ViewResponse(message=message, buttons=buttons)

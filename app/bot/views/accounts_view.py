"""Views for accounts management"""

from textwrap import dedent

from telethon import Button

from app.bot.views import ViewResponse
from app.bot.views.shared_view import get_main_keyboard
from app.database.models import Account
from app.utils.language import Translator


def render_accounts_message(
    accounts: list[Account], default_account_id: int | None, translator: Translator
) -> ViewResponse:
    """Render the accounts management message."""
    message = f"<b>{translator.get('accountsBtn')}</b>\n\n"
    message += f"{translator.get('totalAccountsLabel')} {len(accounts)}"

    buttons = []
    for account in accounts:
        is_active = account.id == default_account_id
        username = account.username or account.email or f"Account {account.id}"
        account_label = f"{translator.get('activeAccountEmoji')} {username}" if is_active else username
        row = [
            Button.inline(account_label, f"switch_account_{account.id}".encode()),
            Button.inline(translator.get("logoutBtn"), f"logout_account_{account.id}".encode()),
        ]
        buttons.append(row)

    add_account_text = translator.get("addAccountBtn")
    buttons.append([Button.inline(add_account_text, b"login")])
    buttons.append([Button.url(translator.get("signupBtn"), "https://www.seedr.cc")])

    return ViewResponse(message=message, buttons=buttons)


def render_account_not_found(translator: Translator) -> ViewResponse:
    """Render the account not found message."""
    keyboard = get_main_keyboard(has_accounts=False, translator=translator)
    return ViewResponse(message=translator.get("accountNotFound"), buttons=keyboard)


def render_logout_account_confirmation(account_id: int, username: str, translator: Translator) -> ViewResponse:
    """Render the logout account confirmation message."""
    message = dedent(f"""
        <b>{translator.get("confirmLogout")}</b>

        {translator.get("confirmLogoutAccount").format(username=username)}

        {translator.get("actionCannotBeUndoneLogout")}
    """)
    buttons = [
        [
            Button.inline(translator.get("yesBtn"), f"confirm_logout_{account_id}".encode()),
            Button.inline(translator.get("noBtn"), b"cancel_logout"),
        ]
    ]
    return ViewResponse(message=message.strip(), buttons=buttons)


def render_no_account(translator: Translator) -> ViewResponse:
    """Render the no account message."""
    keyboard = get_main_keyboard(has_accounts=False, translator=translator)
    return ViewResponse(message=translator.get("noAccount"), buttons=keyboard)

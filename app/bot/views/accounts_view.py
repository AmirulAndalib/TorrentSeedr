"""Views for accounts management"""

from telethon import Button

from app.bot.views import ViewResponse
from app.database.models import Account
from app.utils.language import Translator


def render_accounts_message(
    accounts: list[Account], default_account_id: int | None, translator: Translator
) -> ViewResponse:
    """Render the accounts management message and buttons."""
    message = f"<b>{translator.get('accountsBtn')}</b>\n\n"
    message += f"{translator.get('totalAccountsLabel')}: {len(accounts)}"

    buttons = []
    for account in accounts:
        is_active = account.id == default_account_id
        username = account.username or account.email or f"Account {account.id}"
        account_label = f"✓ {username}" if is_active else username
        row = [
            Button.inline(account_label, f"switch_account_{account.id}".encode()),
            Button.inline(translator.get("deleteEmoji"), f"delete_account_{account.id}".encode()),
        ]
        buttons.append(row)

    add_account_text = translator.get("addAccountBtn")
    buttons.append([Button.inline(add_account_text, b"login")])
    buttons.append([Button.url(translator.get("signupBtn"), "https://www.seedr.cc")])

    return ViewResponse(message=message, buttons=buttons)

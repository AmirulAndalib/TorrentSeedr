"""Views for account information."""

from seedrcc.models import AccountInfo

from app.bot.views import ViewResponse
from app.utils import format_size, progress_bar
from app.utils.language import Translator


def render_account_info(account_info: AccountInfo, translator: Translator) -> ViewResponse:
    username = account_info.username
    email = account_info.email
    user_id = account_info.user_id
    space_used = account_info.space_used
    space_max = account_info.space_max
    bandwidth_used = account_info.bandwidth_used
    premium = translator.get("yesLabel") if bool(account_info.premium) else translator.get("noLabel")
    invites = account_info.invites
    referral_link = f"https://www.seedr.cc/?r={user_id}"

    progress = (space_used / space_max) * 100 if space_max > 0 else 0
    space_bar_visual = progress_bar(progress)

    message = f"<b>{translator.get('accountInfoBtn')}</b>\n\n"
    message += f"<b>{translator.get('usernameLabel')}</b> <code>{username}</code>\n"
    message += f"<b>{translator.get('emailLabel')}</b> <code>{email}</code>\n"
    message += f"<b>{translator.get('premiumLabel')}</b> {premium}\n\n"

    message += f"<b><u>{translator.get('storageLabel')}</u></b>\n"
    message += f"<b>{translator.get('usedLabel')}</b> {format_size(space_used)} / {format_size(space_max)}\n"
    message += f"{space_bar_visual}\n\n"

    message += f"<b>{translator.get('bandwidthUsedLabel')}</b> {format_size(bandwidth_used)}\n"
    message += f"<b>{translator.get('invitesAvailableLabel')}</b> {invites}\n"
    message += f"<b>{translator.get('referralLinkLabel')}</b> <code>{referral_link}</code>"

    return ViewResponse(message=message)


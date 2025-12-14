"""Views for account information."""

from textwrap import dedent

from seedrcc.models import AccountInfo

from app.bot.views import ViewResponse
from app.utils import format_size, progress_bar
from app.utils.language import Translator


def render_account_info(account_info: AccountInfo, translator: Translator) -> ViewResponse:
    username = account_info.username
    bandwidth_used = account_info.bandwidth_used
    invites_remaining = account_info.invites
    invites_accepted = account_info.invites_accepted
    space_used = account_info.space_used
    space_max = account_info.space_max
    referral_link = f"https://www.seedr.cc/?r={account_info.user_id}"

    progress = (space_used / space_max) * 100 if space_max > 0 else 0
    space_bar_visual = progress_bar(progress, translator)

    message = dedent(f"""
        <b>{translator.get("accountInfoBtn")}</b>

        <b>{translator.get("usernameLabel")}</b> <code>{username}</code>
        <b>{translator.get("bandwidthUsedTotalLabel")}</b> {format_size(bandwidth_used)}
        <b>{translator.get("inviteLinkLabel")}</b> <code>{referral_link}</code>
        <b>{translator.get("invitesAvailableLabel")}</b> {invites_remaining} / {account_info.max_invites}
        <b>{translator.get("invitesAcceptedLabel")}</b> {invites_accepted}

        <b>{translator.get("storageLabel")}</b> {format_size(space_used)} / {format_size(space_max)}
        {space_bar_visual}
    """)

    return ViewResponse(message=message.strip())

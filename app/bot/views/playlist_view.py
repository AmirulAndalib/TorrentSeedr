"""Views for playlist-related actions."""

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_playlist_message(
    playlist_type: str,
    media_type: str,
    media_id_str: str,
    translator: Translator,
) -> ViewResponse:
    """Render the message for playlist file."""
    caption = translator.get("openInMediaCaption")
    buttons = [
        [
            Button.inline(
                ("✅ " if playlist_type == "vlc" else "") + translator.get("vlcBtn"),
                f"playlist_vlc_{media_type}_{media_id_str}".encode(),
            ),
            Button.inline(
                ("✅ " if playlist_type == "m3u" else "") + translator.get("m3uBtn"),
                f"playlist_m3u_{media_type}_{media_id_str}".encode(),
            ),
            Button.inline(
                ("✅ " if playlist_type == "xspf" else "") + translator.get("xspfBtn"),
                f"playlist_xspf_{media_type}_{media_id_str}".encode(),
            ),
        ]
    ]
    return ViewResponse(message=caption, buttons=buttons)

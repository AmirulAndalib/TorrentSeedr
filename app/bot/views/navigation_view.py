from textwrap import dedent

from telethon import Button

from app.bot.views import ViewResponse
from app.config import settings
from app.utils import format_size
from app.utils.language import Translator


def render_folder_contents_message(contents, folder_id, parent_id, page: int, translator: Translator) -> ViewResponse:
    """Render the folder contents message and buttons with pagination."""
    parent_id = parent_id or "0"

    # Message for root folder
    if folder_id == "0":
        message_prefix = dedent(f"""
            <b>{translator.get("fileManagerBtn")} - {translator.get("rootLabel")}</b>

            <i>{len(contents.folders)} {translator.get("foldersLabel")}</i>
        """)
    # For normal folder
    else:
        message_prefix = dedent(f"""
            <b>{translator.get("folderEmoji")} {contents.name}</b>

            {translator.get("foldersLabel")}: {len(contents.folders)}
            {translator.get("filesLabel")}: {len(contents.files)}
            {translator.get("totalSizeLabel")}: {format_size(sum(f.size for f in contents.files))}
        """)

    all_items = contents.folders + contents.files
    total_items = len(all_items)
    total_pages = (total_items + settings.page_size - 1) // settings.page_size

    message_pagination = ""
    if total_pages > 1:
        message_pagination = f"{translator.get('pageLabel')}: {page}/{total_pages}"

    message = f"{message_prefix.strip()}\n\n{message_pagination.strip()}"

    start_index = (page - 1) * settings.page_size
    end_index = start_index + settings.page_size
    paginated_items = all_items[start_index:end_index]

    buttons = []
    for item in paginated_items:
        if hasattr(item, "folder_file_id"):  # It's a file
            callback_parts = [
                f"file_{item.folder_file_id}",
                f"parent_{folder_id}",
            ]
            emoji = translator.get("fileEmoji")
            if item.play_video:
                emoji = translator.get("videoEmoji")
                callback_parts.append("type_video")
            elif item.play_audio:
                emoji = translator.get("audioEmoji")
                callback_parts.append("type_audio")

            buttons.append(
                [
                    Button.inline(
                        f"{emoji} {item.name}",
                        "_".join(callback_parts).encode(),
                    )
                ]
            )
        else:  # It's a folder
            buttons.append(
                [
                    Button.inline(
                        f"{translator.get('folderEmoji')} {item.name}",
                        f"folder_{item.id}_page_{page}_parent_{folder_id}".encode(),
                    )
                ]
            )

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            Button.inline(
                translator.get("previousBtn"), f"folder_{folder_id}_parent_{parent_id}_page_{page - 1}".encode()
            )
        )
    if page < total_pages:
        pagination_buttons.append(
            Button.inline(translator.get("nextBtn"), f"folder_{folder_id}_parent_{parent_id}_page_{page + 1}".encode())
        )

    if pagination_buttons:
        buttons.append(pagination_buttons)

    # Don't show action buttons for root folder
    if folder_id != "0":
        buttons.append(
            [
                Button.inline(translator.get("deleteBtn"), f"delete_folder_{folder_id}".encode()),
                Button.inline(translator.get("getLinkBtn"), f"folder_link_{folder_id}".encode()),
            ]
        )
        back_button = Button.inline(translator.get("backBtn"), f"folder_{parent_id}".encode())
        buttons.append(
            [
                Button.inline(translator.get("playlistBtn"), f"playlist_m3u_folder_{folder_id}".encode()),
                back_button,
            ]
        )

    return ViewResponse(message=message.strip(), buttons=buttons)


def render_file_details_message(
    file_metadata,
    is_video: bool,
    is_audio: bool,
    file_id: str,
    parent_folder_id: str | None,
    playlist_format: str,
    translator: Translator,
) -> ViewResponse:
    """Render the file details message and buttons."""
    file_type = (
        f"{translator.get('videoEmoji')} {translator.get('videoLabel')}"
        if is_video
        else f"{translator.get('audioEmoji')} {translator.get('audioLabel')}"
        if is_audio
        else f"{translator.get('fileEmoji')} {translator.get('fileLabel')}"
    )
    message = dedent(f"""
        <b>{translator.get("fileEmoji")} {file_metadata.name}</b>

        {translator.get("sizeLabel")}: {format_size(file_metadata.size)}
        {translator.get("typeLabel")}: {file_type}
    """)

    buttons = [
        [
            Button.inline(translator.get("deleteBtn"), f"delete_file_{file_id}".encode()),
            Button.inline(translator.get("getLinkBtn"), f"file_link_{file_id}".encode()),
        ]
    ]
    if is_video or is_audio:
        buttons.append(
            [
                Button.inline(
                    f"{translator.get('playlistBtn')}",
                    f"playlist_{playlist_format}_file_{file_id}".encode(),
                )
            ]
        )

    back_button = Button.inline(translator.get("backBtn"), f"folder_{parent_folder_id or '0'}".encode())
    buttons.append([back_button])

    return ViewResponse(message=message.strip(), buttons=buttons)

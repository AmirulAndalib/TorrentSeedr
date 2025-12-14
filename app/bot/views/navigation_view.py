"""Views for navigating folders and files."""

from textwrap import dedent

from seedrcc.models import File, Folder, ListContentsResult
from telethon import Button

from app.bot.views import ViewResponse
from app.config import settings
from app.utils import format_date, format_size
from app.utils.language import Translator


def _build_folder_header(
    contents: ListContentsResult, folder_id: str, page: int, total_pages: int, translator: Translator
) -> str:
    """Builds the text header for the folder contents message."""
    if folder_id == "0":
        name = f"{translator.get('fileManagerBtn')} - {translator.get('rootLabel')}"
        total_size = contents.space_used
    else:
        name = f"{translator.get('folderEmoji')} {contents.name}"
        total_size = sum(f.size for f in contents.files) + sum(f.size for f in contents.folders)

    message_prefix = dedent(f"""
        <b>{name}</b>

        <i>{translator.get("foldersLabel")} {len(contents.folders)}
        {translator.get("filesLabel")} {len(contents.files)}
        {translator.get("sizeLabel")} {format_size(total_size)}
        {translator.get("lastUpdatedLabel")} {format_date(contents.last_update)}</i>
    """)

    message_pagination = ""
    if total_pages > 1:
        message_pagination = f"\n{translator.get('pageLabel')} {page}/{total_pages}"

    return f"{message_prefix.strip()}{message_pagination}"


def _build_item_buttons(folders: list[Folder], files: list[File], folder_id: str, translator: Translator) -> list:
    """Builds the list of buttons for files and folders."""
    buttons = []
    for folder in folders:
        buttons.append(
            [
                Button.inline(
                    f"{translator.get('folderEmoji')} {folder.name}",
                    f"folder_{folder.id}_page_1_parent_{folder_id}".encode(),
                )
            ]
        )

    for file in files:
        emoji = translator.get("fileEmoji")
        if file.play_video:
            emoji = translator.get("videoEmoji")
        elif file.play_audio:
            emoji = translator.get("audioEmoji")
        buttons.append([Button.inline(f"{emoji} {file.name}", f"file_{file.folder_file_id}_parent_{folder_id}")])

    return buttons


def _build_pagination_buttons(
    folder_id: str, parent_id: str, page: int, total_pages: int, translator: Translator
) -> list:
    """Builds the pagination buttons (Previous/Next)."""
    buttons = []
    if page > 1:
        buttons.append(
            Button.inline(
                translator.get("previousBtn"), f"folder_{folder_id}_parent_{parent_id}_page_{page - 1}".encode()
            )
        )
    if page < total_pages:
        buttons.append(
            Button.inline(translator.get("nextBtn"), f"folder_{folder_id}_parent_{parent_id}_page_{page + 1}".encode())
        )
    return buttons


def _build_action_buttons(folder_id: str, parent_id: str, translator: Translator) -> list:
    """Builds the action buttons (Delete, Get Link, Back, etc.)."""
    return [
        [
            Button.inline(translator.get("deleteBtn"), f"delete_folder_{folder_id}".encode()),
            Button.inline(translator.get("getLinkBtn"), f"folder_link_{folder_id}".encode()),
        ],
        [
            Button.inline(translator.get("playlistBtn"), f"playlist_m3u_folder_{folder_id}".encode()),
            Button.inline(translator.get("backBtn"), f"folder_{parent_id}".encode()),
        ],
    ]


def render_folder_contents_message(
    contents: ListContentsResult, folder_id: str, parent_id: str | None, page: int, translator: Translator
) -> ViewResponse:
    """Render the folder contents message and buttons with pagination."""
    parent_id = parent_id or "0"
    all_items = contents.folders + contents.files
    total_pages = (len(all_items) + settings.page_size - 1) // settings.page_size

    start_index = (page - 1) * settings.page_size
    end_index = start_index + settings.page_size

    paginated_folders = [item for item in contents.folders if start_index <= all_items.index(item) < end_index]
    paginated_files = [item for item in contents.files if start_index <= all_items.index(item) < end_index]

    message = _build_folder_header(contents, folder_id, page, total_pages, translator)

    buttons = _build_item_buttons(paginated_folders, paginated_files, folder_id, translator)

    pagination_row = _build_pagination_buttons(folder_id, parent_id, page, total_pages, translator)
    if pagination_row:
        buttons.append(pagination_row)

    if folder_id != "0":
        action_buttons = _build_action_buttons(folder_id, parent_id, translator)
        buttons.extend(action_buttons)

    return ViewResponse(message=message.strip(), buttons=buttons)


def render_file_details_message(
    file_metadata: File,
    playlist_format: str,
    translator: Translator,
) -> ViewResponse:
    """Render the file details message and buttons."""
    file_id = file_metadata.folder_file_id
    emoji = (
        translator.get("videoEmoji")
        if file_metadata.play_video
        else translator.get("audioEmoji")
        if file_metadata.play_audio
        else translator.get("fileEmoji")
    )

    message = dedent(f"""
        <b>{emoji} {file_metadata.name}</b>

        <i>{translator.get("sizeLabel")} {format_size(file_metadata.size)}
        {translator.get("lastUpdatedLabel")} {format_date(file_metadata.last_update)}</i>
    """)

    buttons = [
        [
            Button.inline(translator.get("deleteBtn"), f"delete_file_{file_id}".encode()),
            Button.inline(translator.get("getLinkBtn"), f"file_link_{file_id}".encode()),
        ]
    ]
    if file_metadata.play_audio or file_metadata.play_video:
        buttons.append(
            [
                Button.inline(
                    f"{translator.get('playlistBtn')}",
                    f"playlist_{playlist_format}_file_{file_id}".encode(),
                )
            ]
        )

    back_button = Button.inline(translator.get("backBtn"), f"folder_{file_metadata.folder_id or '0'}".encode())
    buttons.append([back_button])

    return ViewResponse(message=message.strip(), buttons=buttons)

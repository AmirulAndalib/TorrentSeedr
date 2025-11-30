from telethon import Button

from app.bot.views import ViewResponse
from app.config import settings
from app.utils import format_size
from app.utils.language import Translator


def render_files_message(folders, translator: Translator) -> ViewResponse:
    """Render the file manager message and buttons for root folder."""
    message = f"<b>{translator.get('fileManagerBtn')} - {translator.get('rootLabel')}</b>\n\n"
    message += f"<i>{len(folders)} {translator.get('foldersLabel')}</i>"

    buttons = [[Button.inline(f"{translator.get('folderEmoji')} {f.name}", f"folder_{f.id}".encode())] for f in folders]
    return ViewResponse(message=message, buttons=buttons)


def render_folder_contents_message(contents, folder_id, parent_id, page: int, translator: Translator) -> ViewResponse:
    """Render the folder contents message and buttons with pagination."""
    message = f"<b>{translator.get('folderEmoji')} {contents.name}</b>\n\n"

    all_items = contents.folders + contents.files
    total_items = len(all_items)
    total_pages = (total_items + settings.page_size - 1) // settings.page_size

    start_index = (page - 1) * settings.page_size
    end_index = start_index + settings.page_size
    paginated_items = all_items[start_index:end_index]

    message += f"{translator.get('foldersLabel')}: {len(contents.folders)}\n"
    message += f"{translator.get('filesLabel')}: {len(contents.files)}\n"
    message += f"{translator.get('totalSizeLabel')}: {format_size(sum(f.size for f in contents.files))}\n"
    if total_pages > 1:
        message += f"{translator.get('pageLabel')}: {page}/{total_pages}\n"
    message += "\n"

    buttons = []
    for item in paginated_items:
        if hasattr(item, "folder_file_id"):  # It's a file
            emoji = translator.get("fileEmoji")
            callback_suffix = ""
            if item.play_video:
                emoji = translator.get("videoEmoji")
                callback_suffix = "_video"
            elif item.play_audio:
                emoji = translator.get("audioEmoji")
                callback_suffix = "_audio"

            buttons.append(
                [
                    Button.inline(
                        f"{emoji} {item.name}",
                        f"file_{item.folder_file_id}_parent_{folder_id}{callback_suffix}".encode(),
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
            Button.inline(translator.get("previousBtn"), f"folder_{folder_id}_page_{page - 1}".encode())
        )
    if page < total_pages:
        pagination_buttons.append(
            Button.inline(translator.get("nextBtn"), f"folder_{folder_id}_page_{page + 1}".encode())
        )

    if pagination_buttons:
        buttons.append(pagination_buttons)

    buttons.append(
        [
            Button.inline(translator.get("deleteBtn"), f"delete_folder_{folder_id}".encode()),
            Button.inline(translator.get("getLinkBtn"), f"folder_link_{folder_id}".encode()),
        ]
    )
    back_button = (
        Button.inline(translator.get("backBtn"), b"folder_back")
        if parent_id is None
        else Button.inline(translator.get("backBtn"), f"folder_{parent_id}".encode())
    )
    buttons.append(
        [
            Button.inline(translator.get("playlistBtn"), f"playlist_m3u_folder_{folder_id}".encode()),
            back_button,
        ]
    )

    return ViewResponse(message=message, buttons=buttons)


def render_file_details_message(
    file_metadata,
    url: str | None,
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
    message = f"<b>{translator.get('fileEmoji')} {file_metadata.name}</b>\n\n"
    message += f"{translator.get('sizeLabel')}: {format_size(file_metadata.size)}\n"
    message += f"{translator.get('typeLabel')}: {file_type}\n\n"

    if url:
        message += (
            f"{translator.get('downloadUrlLabel')}:\n"
            f"<code>{url}</code>\n\n"
            f"<a href='{url}'>{translator.get('clickToDownloadLabel')}</a>\n"
        )

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
                    f"{translator.get('playlistBtn')} ({playlist_format.upper()})",
                    f"playlist_{playlist_format}_file_{file_id}".encode(),
                )
            ]
        )

    back_button = (
        Button.inline(translator.get("backBtn"), b"folder_back")
        if parent_folder_id is None
        else Button.inline(translator.get("backBtn"), f"folder_{parent_folder_id}".encode())
    )
    buttons.append([back_button])

    return ViewResponse(message=message, buttons=buttons)


def render_file_link_message(file_result, translator: Translator) -> ViewResponse:
    """Render the file download link message."""
    message = (
        f"<b>{translator.get('fileEmoji')} {file_result.name}</b>\n\n"
        f"<b>{translator.get('downloadLinkLabel')}</b>:\n"
        f"<code>{file_result.url}</code>"
    )
    buttons = [[Button.url(translator.get("downloadFileBtn"), file_result.url)]]
    return ViewResponse(message=message, buttons=buttons)


def render_folder_link_message(archive_url: str, translator: Translator) -> ViewResponse:
    """Render the folder download link message."""
    message = (
        f"<b>{translator.get('folderEmoji')} {translator.get('folderDownloadLinkLabel')}</b>\n\n"
        f"<b>{translator.get('downloadLinkLabel')}</b>:\n"
        f"<code>{archive_url}</code>"
    )
    buttons = [[Button.url(translator.get("downloadFolderBtn"), archive_url)]]
    return ViewResponse(message=message, buttons=buttons)


def render_failed_to_delete_file_message(translator: Translator) -> ViewResponse:
    """Render the message for failed file deletion."""
    message = translator.get("somethingWrong")
    return ViewResponse(message=message)


def render_failed_to_delete_folder_message(translator: Translator) -> ViewResponse:
    """Render the message for failed folder deletion."""
    message = translator.get("somethingWrong")
    return ViewResponse(message=message)


def render_no_files_message(translator: Translator) -> ViewResponse:
    """Render the message for when there are no files."""
    return ViewResponse(message=translator.get("noFiles"))


def render_error_fetching_link_message(translator: Translator) -> ViewResponse:
    """Render the message for an error fetching a link."""
    return ViewResponse(message=translator.get("errorFetchingLink"))

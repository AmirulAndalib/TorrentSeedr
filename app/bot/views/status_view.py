"""Views for status and error messages related to file operations."""

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_deleted_successfully_message(translator: Translator) -> ViewResponse:
    """Render the message for successful deletion of file or folder."""
    message = translator.get("deletedSuccessfully")
    return ViewResponse(message=message)


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

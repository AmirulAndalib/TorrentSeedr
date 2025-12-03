"""Custom decorators for handlers."""

import functools
import inspect
from typing import Any

from seedrcc import AsyncSeedr, Token
from seedrcc.exceptions import APIError, AuthenticationError, SeedrError
from structlog import get_logger
from telethon import events, errors

from app.database import get_session
from app.database.repository import AccountRepository, UserRepository
from app.services.seedr import on_token_refresh
from app.utils.language import get_language_service
from app.exceptions import NoAccountError

logger = get_logger(__name__)
language_service = get_language_service()


def setup_handler(require_auth: bool = False):
    """
    The primary decorator for all handlers. It provides:
    1.  Session management.
    2.  User and translator dependency injection.
    3.  Optional authentication and Seedr client injection.
    TODO: Refactor into multiple function but a single decorator
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event: events.NewMessage.Event | events.CallbackQuery.Event, *args: Any, **kwargs: Any):
            translator = None

            try:
                async with get_session() as session:
                    user = await UserRepository(session).get_or_create(event.sender_id)
                    translator = language_service.get_translator(user.language)

                    dependencies = {
                        "event": event,
                        "user": user,
                        "translator": translator,
                        "client": event.client,
                    }

                    if require_auth:
                        if not user.default_account_id:
                            raise NoAccountError(translator.get("noAccount"))

                        account = await AccountRepository(session).get_by_id(user.default_account_id)
                        if not account:
                            raise NoAccountError(translator.get("noAccount"))

                        token_instance = Token.from_base64(account.token)
                        callback = functools.partial(on_token_refresh, account_id=account.id)
                        seedr_client = AsyncSeedr(token=token_instance, on_token_refresh=callback)

                        dependencies["seedr_client"] = seedr_client

                    handler_signature = inspect.signature(func)
                    final_kwargs = {
                        key: value for key, value in dependencies.items() if key in handler_signature.parameters
                    }

                    return await func(**final_kwargs)

            except events.StopPropagation:
                raise

            except NoAccountError as e:
                if translator:
                    error_message = str(e)
                    if isinstance(event, events.CallbackQuery.Event):
                        await event.answer(error_message, alert=True)
                    else:
                        await event.respond(error_message)
                logger.warning(f"NoAccountError in {func.__name__}: {e}", exc_info=True)
                raise events.StopPropagation()

            except AuthenticationError as e:
                if translator:
                    error_message = str(e) or translator.get("tokenExpired")
                    if isinstance(event, events.CallbackQuery.Event):
                        await event.answer(error_message, alert=True)
                    else:
                        await event.respond(error_message)
                logger.warning(f"AuthenticationError in {func.__name__}: {e}", exc_info=True)
                raise events.StopPropagation()

            except (APIError, SeedrError) as e:
                if translator:
                    error_message = translator.get("somethingWrong")
                    if isinstance(event, events.CallbackQuery.Event):
                        await event.answer(error_message, alert=True)
                    else:
                        await event.respond(error_message)
                logger.error(f"APIError/SeedrError in {func.__name__}: {e}", exc_info=True)
                raise events.StopPropagation()

            except errors.AlreadyInConversationError:
                logger.warning(f"AlreadyInConversationError in {func.__name__}")
                raise events.StopPropagation()

            except Exception as e:
                if translator:
                    error_message = translator.get("somethingWrong")
                    if isinstance(event, events.CallbackQuery.Event):
                        await event.answer(error_message, alert=True)
                    else:
                        await event.respond(error_message)
                logger.error(f"Unhandled exception in {func.__name__}: {e}", exc_info=True)
                raise events.StopPropagation()

        return wrapper

    return decorator

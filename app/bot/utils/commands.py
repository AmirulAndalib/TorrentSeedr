"""Utility functions for setting bot commands."""

from telethon import events
from telethon.tl import functions, types

from app.utils.language import Translator


async def set_user_commands(
    event: events.NewMessage.Event,
    translator: Translator,
    has_accounts: bool,
):
    base_commands = [
        types.BotCommand(command="start", description=translator.get("startCmdDesc")),
        types.BotCommand(command="login", description=translator.get("loginCmdDesc")),
        types.BotCommand(command="signup", description=translator.get("signupCmdDesc")),
    ]

    if has_accounts:
        account_commands = [
            types.BotCommand(command="files", description=translator.get("filesCmdDesc")),
            types.BotCommand(command="active", description=translator.get("activeCmdDesc")),
            types.BotCommand(command="info", description=translator.get("infoCmdDesc")),
            types.BotCommand(command="accounts", description=translator.get("accountsCmdDesc")),
        ]
        commands = base_commands + account_commands
    else:
        commands = base_commands

    await event.client(
        functions.bots.SetBotCommandsRequest(
            scope=types.BotCommandScopePeer(peer=await event.get_input_sender()),
            lang_code="",
            commands=commands,
        )
    )

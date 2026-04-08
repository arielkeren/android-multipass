import enum
import logging
import argparse
import frida

SCRIPT_PATH = "hook.js"
PROCESS_TO_ATTACH = "system_server"
MESSAGE_EVENT = "message"


class VariableName(enum.StrEnum):
    PASSWORD = "password"
    EXTRA = "extra"
    REGEX = "regex"
    ANAGRAM = "anagram"
    IMMUTABLE = "immutable"
    UNLOCKED = "unlocked"
    LOCKED = "locked"


class MessageType(enum.StrEnum):
    SEND = "send"
    ERROR = "error"


class MessageKey(enum.StrEnum):
    TYPE = "type"
    PAYLOAD = "payload"
    DESCRIPTION = "description"


def on_message(message: dict[str, object], _: bytes | None) -> None:
    if message[MessageKey.TYPE] == MessageType.SEND:
        logging.info(message[MessageKey.PAYLOAD])
    elif message[MessageKey.TYPE] == MessageType.ERROR:
        logging.error(
            f"(Description) {message[MessageKey.DESCRIPTION]}\n(Stack) {message['stack']}"
        )


def inject_hook(args: argparse.Namespace) -> None:
    compiler = frida.Compiler()
    bundle = compiler.build(SCRIPT_PATH)

    session = frida.get_usb_device().attach(PROCESS_TO_ATTACH)
    script = session.create_script(bundle)
    script.on(MESSAGE_EVENT, on_message)
    script.load()

    script.exports_sync.init_config(
        {
            VariableName.PASSWORD: args.password,
            VariableName.EXTRA: args.extra,
            VariableName.REGEX: args.regex,
            VariableName.ANAGRAM: args.anagram,
            VariableName.IMMUTABLE: args.immutable,
            VariableName.UNLOCKED: args.unlocked,
            VariableName.LOCKED: args.locked,
        }
    )

import enum
import logging
import argparse
import frida

SCRIPT_PATH = "hook.js"
PROCESS_TO_ATTACH = "system_server"
MESSAGE_EVENT = "message"


class VariableName(enum.StrEnum):
    PASSWORD = "password"
    ADDITIONAL = "additional"
    REGEX = "regex"
    UNORDERED = "unordered"
    DISABLE = "disable"


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
            VariableName.ADDITIONAL: args.additional,
            VariableName.REGEX: args.regex,
            VariableName.UNORDERED: args.unordered,
            VariableName.DISABLE: args.disable,
        }
    )

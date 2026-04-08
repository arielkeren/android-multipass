import enum
import logging
import argparse
import frida

_SCRIPT_PATH = "hook.js"
_PROCESS_TO_ATTACH = "system_server"
_MESSAGE_EVENT = "message"

_USER_NAME_TO_ID = {
    "null": -10000,
    "frp": -9999,
    "repair": -9998,
}


class _VariableName(enum.StrEnum):
    PASSWORD = "password"
    EXTRA = "extra"
    REGEX = "regex"
    ANAGRAM = "anagram"
    IMMUTABLE = "immutable"
    UNLOCKED = "unlocked"
    LOCKED = "locked"
    USER = "user"


class _MessageType(enum.StrEnum):
    SEND = "send"
    ERROR = "error"


class _MessageKey(enum.StrEnum):
    TYPE = "type"
    PAYLOAD = "payload"
    DESCRIPTION = "description"


def _user_id_to_number(user_id: str | None) -> int | None:
    if user_id is None:
        return None
    if user_id.isdigit() or (user_id.startswith("-") and user_id[1:].isdigit()):
        return int(user_id)
    return _USER_NAME_TO_ID[user_id.lower()]


def _on_message(message: dict[str, object], _: bytes | None) -> None:
    if message[_MessageKey.TYPE] == _MessageType.SEND:
        logging.info(message[_MessageKey.PAYLOAD])
    elif message[_MessageKey.TYPE] == _MessageType.ERROR:
        logging.error(
            f"(Description) {message[_MessageKey.DESCRIPTION]}\n(Stack) {message['stack']}"
        )


def inject_hook(args: argparse.Namespace) -> None:
    compiler = frida.Compiler()
    bundle = compiler.build(_SCRIPT_PATH)

    session = frida.get_usb_device().attach(_PROCESS_TO_ATTACH)
    script = session.create_script(bundle)
    script.on(_MESSAGE_EVENT, _on_message)
    script.load()

    script.exports_sync.init_config(
        {
            _VariableName.PASSWORD: args.password,
            _VariableName.EXTRA: args.extra,
            _VariableName.REGEX: args.regex,
            _VariableName.ANAGRAM: args.anagram,
            _VariableName.IMMUTABLE: args.immutable,
            _VariableName.UNLOCKED: args.unlocked,
            _VariableName.LOCKED: args.locked,
            _VariableName.USER: _user_id_to_number(args.user),
        }
    )

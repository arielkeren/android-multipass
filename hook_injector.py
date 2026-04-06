import argparse
import frida

SCRIPT_PATH = "hook.js"
PROCESS_TO_ATTACH = "system_server"

ACTUAL_PASSWORD_VARIABLE_NAME = "actualPassword"
ADDITIONAL_PASSWORDS_VARIABLE_NAME = "additionalPasswords"


def inject_hook(args: argparse.Namespace) -> None:
    compiler = frida.Compiler()
    bundle = compiler.build(SCRIPT_PATH)

    session = frida.get_usb_device().attach(PROCESS_TO_ATTACH)
    script = session.create_script(bundle)
    script.load()

    script.exports_sync.init_config(
        {
            ACTUAL_PASSWORD_VARIABLE_NAME: args.actual_password,
            ADDITIONAL_PASSWORDS_VARIABLE_NAME: args.additional_passwords,
        }
    )

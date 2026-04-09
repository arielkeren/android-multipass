import argparse
from .validation import validate_arguments

_ALWAYS_REJECTING_REGEX = "(?!)"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set complex passwords for your Android device using Frida",
    )
    parser.add_argument(
        "--password",
        help="The real device password (instead of waiting it to be discovered)",
    )
    parser.add_argument(
        "--extra",
        nargs="+",
        default=[],
        help="One or more extra passwords that should be accepted",
    )
    parser.add_argument(
        "--regex",
        default=_ALWAYS_REJECTING_REGEX,
        help="Accept passwords matching a regular expression",
    )
    parser.add_argument(
        "--anagram",
        action="store_true",
        help="Accept any anagram of the real/additional passwords (any order of the same characters)",
    )
    parser.add_argument(
        "--immutable",
        action="store_true",
        help="Make the password immutable (don't allow changing passwords)",
    )
    parser.add_argument(
        "--unlocked",
        action="store_true",
        help="Unlock the device (accept any password)",
    )
    parser.add_argument(
        "--locked",
        action="store_true",
        help="Lock the device (accept no passwords)",
    )
    parser.add_argument(
        "--user", help="The user ID to use (number or 'null', 'frp' or 'repair')"
    )
    arguments = parser.parse_args()
    validate_arguments(arguments)
    return arguments

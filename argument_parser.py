import argparse
import re

ALWAYS_REJECTING_REGEX = "(?!)"


def is_valid_password(password: str) -> bool:
    return len(password) >= 4


def validate_password(password: str) -> None:
    if not is_valid_password(password):
        raise ValueError(
            f"Invalid real device password '{password}': Passwords must be at least 4 characters long"
        )


def validate_extra_passwords(extra_passwords: list[str]) -> None:
    for i, password in enumerate(extra_passwords):
        if not is_valid_password(password):
            raise ValueError(
                f"Invalid extra password '{password}' (#{i + 1}): Passwords must be at least 4 characters long"
            )


def validate_regex(regex: str) -> None:
    try:
        re.compile(regex)
    except re.error:
        raise ValueError(f"Invalid regex pattern '{regex}'")


def validate_locked_unlocked(locked: bool, unlocked: bool) -> None:
    if locked and unlocked:
        raise ValueError("Cannot specify both '--locked' and '--unlocked'")


def validate_arguments(args: argparse.Namespace) -> None:
    validate_password(args.password)
    validate_extra_passwords(args.extra)
    validate_regex(args.regex)
    validate_locked_unlocked(args.locked, args.unlocked)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set complex passwords for your Android device using Frida",
    )
    parser.add_argument(
        "-p",
        "--password",
        required=True,
        help="The real device password",
    )
    parser.add_argument(
        "-e",
        "--extra",
        nargs="+",
        default=[],
        help="One or more extra passwords that should be accepted",
    )
    parser.add_argument(
        "-r",
        "--regex",
        default=ALWAYS_REJECTING_REGEX,
        help="Accept passwords matching a regular expression",
    )
    parser.add_argument(
        "-a",
        "--anagram",
        action="store_true",
        help="Accept any anagram of the real/additional passwords (any order of the same characters)",
    )
    parser.add_argument(
        "-i",
        "--immutable",
        action="store_true",
        help="Make the password immutable (don't allow changing passwords)",
    )
    parser.add_argument(
        "-u",
        "--unlocked",
        action="store_true",
        help="Unlock the device (accept any password)",
    )
    parser.add_argument(
        "-l",
        "--locked",
        action="store_true",
        help="Lock the device (accept no passwords)",
    )
    arguments = parser.parse_args()
    validate_arguments(arguments)
    return arguments

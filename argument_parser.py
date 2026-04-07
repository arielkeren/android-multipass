import argparse
import re

ALWAYS_REJECTING_REGEX = "(?!)"


def is_valid_password(password: str) -> bool:
    return len(password) >= 4


def validate_additional_passwords(additional_passwords: list[str]) -> None:
    for i, password in enumerate(additional_passwords):
        if not is_valid_password(password):
            raise ValueError(
                f"Invalid additional password '{password}' (#{i + 1}): Passwords must be at least 4 characters long"
            )


def validate_regex(regex: str) -> None:
    try:
        re.compile(regex)
    except re.error:
        raise ValueError(f"Invalid regex pattern '{regex}'")


def validate_arguments(args: argparse.Namespace) -> None:
    if not is_valid_password(args.password):
        raise ValueError(
            f"Invalid real device password '{args.password}': Passwords must be at least 4 characters long"
        )
    validate_additional_passwords(args.additional)
    validate_regex(args.regex)


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
        "-a",
        "--additional",
        nargs="+",
        default=[],
        help="One or more additional passwords that should be accepted",
    )
    parser.add_argument(
        "-r",
        "--regex",
        default=ALWAYS_REJECTING_REGEX,
        help="A regex pattern for additional passwords that should be accepted",
    )
    parser.add_argument(
        "-u",
        "--unordered",
        action="store_true",
        help="Accept passwords in any order",
    )
    parser.add_argument(
        "-d",
        "--disable",
        action="store_true",
        help="Disable password verification (accept any password)",
    )
    arguments = parser.parse_args()
    validate_arguments(arguments)
    return arguments

import re
import argparse

_ACCEPTED_USER_NAMES = {"null", "frp", "repair"}


def _is_valid_password(password: str) -> bool:
    return len(password) >= 4


def _validate_password(password: str | None) -> None:
    if password is not None and not _is_valid_password(password):
        raise ValueError(
            f"Invalid real device password '{password}': Passwords must be at least 4 characters long"
        )


def _validate_extra_passwords(extra_passwords: list[str]) -> None:
    for i, password in enumerate(extra_passwords):
        if not _is_valid_password(password):
            raise ValueError(
                f"Invalid extra password '{password}' (#{i + 1}): Passwords must be at least 4 characters long"
            )


def _validate_regex(regex: str) -> None:
    try:
        re.compile(regex)
    except re.error:
        raise ValueError(f"Invalid regex pattern '{regex}'")


def _validate_locked_unlocked(locked: bool, unlocked: bool) -> None:
    if locked and unlocked:
        raise ValueError("Cannot specify both '--locked' and '--unlocked'")


def _validate_user(user: str | None) -> None:
    if user is not None and not (
        user.isdigit()
        or (user.startswith("-") and user[1:].isdigit())
        or user.lower() in _ACCEPTED_USER_NAMES
    ):
        raise ValueError(
            f"Invalid user ID '{user}': Must be a number or one of 'null', 'frp', 'repair'"
        )


def validate_arguments(args: argparse.Namespace) -> None:
    _validate_password(args.password)
    _validate_extra_passwords(args.extra)
    _validate_regex(args.regex)
    _validate_locked_unlocked(args.locked, args.unlocked)
    _validate_user(args.user)

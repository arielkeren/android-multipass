import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set multiple passwords for your Android device using Frida",
    )
    parser.add_argument(
        "--actual-password",
        required=True,
        help="The real device password",
    )
    parser.add_argument(
        "--additional-passwords",
        nargs="+",
        required=True,
        help="One or more additional passwords that should be accepted",
    )
    return parser.parse_args()

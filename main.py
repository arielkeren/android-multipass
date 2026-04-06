import sys
from argument_parser import parse_arguments
from hook_injector import inject_hook


def main() -> None:
    arguments = parse_arguments()
    inject_hook(arguments)
    sys.stdin.read()


if __name__ == "__main__":
    main()

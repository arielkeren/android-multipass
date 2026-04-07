import sys
import logging
from argument_parser import parse_arguments
from hook_injector import inject_hook

ERROR_EXIT_CODE = 1
LOG_FORMAT = "[%(levelname)s] %(message)s"


def main() -> None:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    logging.info("Starting Android MultiPass...")

    try:
        arguments = parse_arguments()
    except ValueError as e:
        logging.error(e)
        sys.exit(ERROR_EXIT_CODE)

    logging.info(f"Arguments parsed successfully: {vars(arguments)}")
    inject_hook(arguments)
    logging.info("Hook injected successfully. MultiPass is now active!")
    sys.stdin.read()


if __name__ == "__main__":
    main()

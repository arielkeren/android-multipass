import sys
import logging
from logger_configuration import configure_logger
from arguments import parse_arguments
from hook_injector import inject_hook

ERROR_EXIT_CODE = 1


def main() -> None:
    configure_logger()
    logging.debug("Starting Android MultiPass...")

    try:
        arguments = parse_arguments()
    except ValueError as error:
        logging.error(error)
        sys.exit(ERROR_EXIT_CODE)

    logging.info(f"Arguments parsed successfully: {vars(arguments)}")
    inject_hook(arguments)
    logging.info("Hook injected successfully. MultiPass is now active!")
    sys.stdin.read()


if __name__ == "__main__":
    main()

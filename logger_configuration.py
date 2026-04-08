import enum
import logging


class Color(enum.StrEnum):
    RESET = "\033[0m"
    GRAY = "\033[90m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    DARK_RED = "\033[31m"


class PrefixFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        prefix_map = {
            logging.DEBUG: f"{Color.GRAY}[-]{Color.RESET}",
            logging.INFO: f"{Color.BLUE}[*]{Color.RESET}",
            logging.WARNING: f"{Color.YELLOW}[**]{Color.RESET}",
            logging.ERROR: f"{Color.RED}[!]{Color.RESET}",
            logging.CRITICAL: f"{Color.DARK_RED}[!!]{Color.RESET}",
        }
        prefix = prefix_map.get(record.levelno, f"[{record.levelname}]")
        return f"{prefix} {record.getMessage()}"


def configure_logger() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(PrefixFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)

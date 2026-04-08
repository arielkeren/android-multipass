import enum
import logging


class _Color(enum.StrEnum):
    RESET = "\033[0m"
    GRAY = "\033[90m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    DARK_RED = "\033[31m"


class _PrefixFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        prefix_map = {
            logging.DEBUG: f"{_Color.GRAY}[-]{_Color.RESET}",
            logging.INFO: f"{_Color.BLUE}[*]{_Color.RESET}",
            logging.WARNING: f"{_Color.YELLOW}[**]{_Color.RESET}",
            logging.ERROR: f"{_Color.RED}[!]{_Color.RESET}",
            logging.CRITICAL: f"{_Color.DARK_RED}[!!]{_Color.RESET}",
        }
        prefix = prefix_map.get(record.levelno, f"[{record.levelname}]")
        return f"{prefix} {record.getMessage()}"


def configure_logger() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(_PrefixFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)

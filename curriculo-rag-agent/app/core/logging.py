import logging
import sys
import structlog
from app.core.config import settings

def setup_logging():
    """
    Configures structlog for structured logging.
    In development (standard output), it uses pretty-printing with colors.
    In production (or when configured), it could use JSON format.
    """
    
    # Processors that are used for both standard logging and structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    # If we are in a TTY (terminal), use ConsoleRenderer for pretty logs
    if sys.stderr.isatty():
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    else:
        # Otherwise, use JSON formatting for structured logs (good for ELK/CloudWatch)
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Hook into standard logging as well
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

def get_logger(name: str):
    return structlog.get_logger(name)

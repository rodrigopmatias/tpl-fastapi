from logging.config import dictConfig


def setup() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "style": "{",
                    "format": "{asctime} - {levelname:^7} - {name} - {message}",
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "default",
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["console"], "propagate": False},
                "machine_api": {
                    "handlers": ["console"],
                    "propagate": True,
                    "level": "INFO",
                },
            },
        }
    )

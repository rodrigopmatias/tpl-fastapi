from logging import Formatter, LogRecord
from logging.config import dictConfig
from typing import override

from {{cookiecutter.project_module}}.middlewares import request_id


class InjectExtraFormatter(Formatter):
    @override
    def format(self, record: LogRecord) -> str:
        record.request_id = request_id.restore()
        return super().format(record)


def setup() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "class": "{{cookiecutter.project_module}}.logger.InjectExtraFormatter",
                    "style": "{",
                    "format": "{asctime} - {levelname:^7} - {request_id} - {name} - {message}",
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                    "defaults": {"request_id": "---"},
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
                "{{ cookiecutter.project_module }}": {
                    "handlers": ["console"],
                    "propagate": True,
                    "level": "INFO",
                },
            },
        }
    )

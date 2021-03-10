import sys
import pathlib
import logging

from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(
        self,
        record,
    ) -> None:
        try:
            level = logger.level(
                record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(
            request_id="app")

        log.opt(
            depth=depth,
            exception=record.exc_info).log(
                level,
                record.getMessage())


class Logger:
    def __init__(
        self,
    ) -> logger:
        self.log_path = settings.log_path
        self.log_filename = settings.log_filename
        self.log_level = settings.log_level
        self.log_rotation = settings.log_rotation
        self.log_retention = settings.log_retention
        self.log_format = settings.log_format

    @property
    def path(
        self,
    ) -> pathlib.Path:
        return f"{self.log_path}/{self.log_filename}"

    def make_logger(
        self,
    ):
        logger = self.customize_logging(
            filepath=self.path,
            level=self.log_level,
            rotation=self.log_rotation,
            retention=self.log_retention,
            format=self.log_format
        )

        return logger

    @classmethod
    def customize_logging(
        cls,
        filepath: pathlib.Path,
        level: str,
        rotation: str,
        retention: str,
        format: str,
    ) -> logger:
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        logging.basicConfig(
            handlers=[
                InterceptHandler(),
            ],
            level=0)
        logging.getLogger(
            "uvicorn.access").handlers = [
                InterceptHandler(),
        ]

        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [
                InterceptHandler(),
            ]

        return logger.bind(
            request_id=None,
            method=None)
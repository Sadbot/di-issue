import logging

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger



class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_log.addHandler(handler)
        self.access_log.addHandler(handler)

        self.error_log.setLevel("DEBUG")
        self.access_log.setLevel("DEBUG")

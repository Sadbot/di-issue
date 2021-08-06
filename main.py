import asyncio
import sys

from fastapi import FastAPI

import routes
from container import Container
from gunicorn_app import StandaloneApplication, StubbedGunicornLogger
from logger import init_logger


def create_app():
    app = FastAPI(
        debug=True,
        title="test",
        version="0.1.0",
    )
    app.container = Container()
    app.container.init_resources()
    app.container.wire(packages=[routes])
    app.logger = init_logger("DEBUG")

    app.include_router(routes.api_router)
    return app


def run_gunicorn(app):
    options = {
        "bind": f"0.0.0.0:8888",
        "workers": 1,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger,
        "keep_alive": 2,
        "graceful_timeout": 10,
        "timeout": 10000,
        "reload": True,
    }
    StandaloneApplication(app, options).run()


if __name__ == "__main__":
    app = create_app()
    run_gunicorn(app)

from fastapi import FastAPI
from .models import db
from .config import VERSION
import logging
from importlib.metadata import entry_points

logger = logging.getLogger(__name__)


def load_modules(app=None):
    for ep in entry_points()["library_api.modules"]:
        logger.info("Loading module: %s", ep.name)
        mod = ep.load()
        if app:
            init_app = getattr(mod, "init_app", None)
            if init_app:
                init_app(app)


def get_app():
    app = FastAPI(title=f"library API {VERSION}")
    db.init_app(app=app)
    load_modules(app)
    return app

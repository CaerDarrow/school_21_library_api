from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from .models import db
from .config import VERSION
import logging
from importlib.metadata import entry_points
from starlette.middleware.sessions import SessionMiddleware


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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
    app = FastAPI(
        title=f"library API {VERSION}",
        # dependencies=[Depends(oauth2_scheme)],
    )
    app.add_middleware(SessionMiddleware, secret_key="some-random-string")
    db.init_app(app=app)
    load_modules(app)
    return app

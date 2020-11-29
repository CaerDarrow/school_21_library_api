from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request
import logging

config = Config('.env')
router = APIRouter()
oauth = OAuth(config)
oauth.register(
    name='auth_42',
    access_token_url='https://api.intra.42.fr/oauth/authorize',
    authorize_url='https://api.intra.42.fr/oauth/token',
    client_kwargs={
        'scope': 'public'
    }
)


@router.get("/login/42")
async def login_via_42(request: Request):
    redirect_uri = 'http://localhost:8000/auth/42'
    return await oauth.auth_42.authorize_redirect(request, redirect_uri)


@router.get("/auth/42")
async def auth_via_42(request: Request):
    token = await oauth.auth_42.authorize_access_token(request)
    user = await oauth.gauth_42.parse_id_token(request, token)
    logging.info(user)
    return dict(user)


def init_app(app):
    app.include_router(router)

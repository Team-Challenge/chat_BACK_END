from datetime import datetime
from typing import Annotated

import requests
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from jose import JWTError
from requests import RequestException

from chat.core.config import settings
from chat.core.exceptions import IncorrectTokenFormat, Unauthorized, TokenExpired, NotFound

# Don't use localhost:8080 to avoid slow performance
FLASK_INFO_USER_ID_URL = "http://127.0.0.1:5000/accounts/info/for_chat"
FLASK_INFO_SHOP_ID_URL = "http://127.0.0.1:5000/shops/shop_info/for_chat"
FLASK_INFO_SHOP_OWNER_ID_URL = "http://127.0.0.1:5000/shops/shop_owner_info/for_chat"


auth_scheme = HTTPBearer(scheme_name="TokenScheme", auto_error=True)

session = requests.Session()


def get_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]):
    token = credentials.credentials
    if "Bearer " in token:
        token = token.replace("Bearer ", "")
    if token:
        return token
    raise Unauthorized(detail="Access token is required")


def get_user_id_from_service(token: str) -> int:
    headers = {"Authorization": f"Bearer {token}"}
    response = session.get(FLASK_INFO_USER_ID_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        user_id = data.get("user_id")
        if user_id is not None:
            return user_id
        else:
            raise IncorrectTokenFormat(detail="User ID not found in the response")
    else:
        raise Unauthorized(detail="Invalid token or user not authorized")


def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token format")

    expire: int = payload.get("exp")
    if expire and int(expire) < datetime.now().timestamp():
        raise TokenExpired()

    # Validate token with the external service and get user_id
    user_id = get_user_id_from_service(token)
    return user_id


UserDep = Annotated[int, Depends(get_current_user)]


def check_shop_id(shop_id: int, token: str = Depends(get_token)):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = session.get(f"{FLASK_INFO_SHOP_ID_URL}/{shop_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            shop_owner = data.get("shop_owner")
            if shop_owner is not None:
                return shop_owner
            else:
                raise NotFound(status_code=404, detail="shop_owner not found in response")
        else:
            raise NotFound(status_code=404, detail=f"Shop with id {shop_id} not found")
    except RequestException as e:
        raise HTTPException(status_code=503, detail="Could not connect to the shop service") from e


def get_shop_id_with_token_user(token: str = Depends(get_token)):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = session.get(f"{FLASK_INFO_SHOP_OWNER_ID_URL}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            shop_id = data.get("shop_id")
            if shop_id is not None:
                return shop_id
            else:
                raise NotFound(status_code=404, detail="shop_id not found in response")
        else:
            raise NotFound(status_code=404, detail=f"Owner shop not found")
    except RequestException as e:
        raise HTTPException(status_code=503, detail="Could not connect to the shop service") from e


ShopDep = Annotated[int, Depends(get_shop_id_with_token_user)]
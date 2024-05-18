#

from datetime import datetime, timedelta
from typing import Optional, Annotated

import jwt
import requests
from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from jose import jwt, JWTError

from chat.core.config import settings
from chat.core.exceptions import IncorrectTokenFormat, Unauthorized, TokenExpired, UserIsNotPresent
from chat.database.crud import get_user, create_user
from chat.database.database import dbDep
from chat.database.models import User
from chat.database.schemas import UserCopy

# Don't use localhost:8080 to avoid slow performance
FLASK_INFO_URL = "http://127.0.0.1:8080/accounts/info"

auth_scheme = HTTPBearer(scheme_name="TokenScheme", auto_error=True)


def get_user_info(token, user_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(FLASK_INFO_URL, headers=headers)
    if response.status_code == 200:
        return UserCopy(id=user_id, **response.json())
    else:
        return None


def get_token(token: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]):
    token = token.credentials
    if "Bearer " in token:
        token = token.replace("Bearer ", "")
    if token:
        return token
    raise Unauthorized(detail="Access token is required")


def get_current_user(db: dbDep, token: str = Depends(get_token), ) -> Optional[User]:
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=["HS256"])
    except JWTError as ex:
        if str(ex) == "Signature has expired.":
            raise IncorrectTokenFormat(detail="Signature has expired")
        raise IncorrectTokenFormat(detail="qw")
    expire: str = payload.get("exp")
    if expire and int(expire) < datetime.now().timestamp():
        raise TokenExpired()

    user_id = payload.get("sub")
    if not user_id:
        raise IncorrectTokenFormat()

    user = get_user(db, user_id=user_id)
    if not user:
        user_info = get_user_info(token, user_id=user_id)
        if user_info:
            user = create_user(db, user_info)
            return user
        raise UserIsNotPresent()
    if not user.last_check or user.last_check + timedelta(minutes=5) < datetime.now():
        print("updated")
        user = user.update(get_user_info(token, user_id=user_id))
        db.commit()
    return user


UserDep: User = Annotated[get_current_user, Depends()]

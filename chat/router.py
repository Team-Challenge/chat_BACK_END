from fastapi import APIRouter

from chat.core.dependencies import UserDep
from chat.database.crud import soft_delete_message
from chat.database.database import dbDep

router = APIRouter(tags=["Both"])


@router.delete("/delete_message/{message_id}")
def delete_message(user: UserDep, db: dbDep, message_id: int):
    return soft_delete_message(db, user, message_id)

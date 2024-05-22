from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from chat.core.dependencies import UserDep
from chat.database.crud import (get_or_create_chat, create_message, get_messages,
                                get_chats_by_customer_id)
from chat.database.database import dbDep
from chat.database.schemas import MessageSchema, CustomerMessageCreateSchema, ChatModelSchema
from chat.core.exceptions import BadRequest

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.post("/create_chat")
def create_chat(user_id: UserDep, db: dbDep, shop_id):
    if shop_id is not int:
        raise BadRequest(status_code=400, detail="shop_id must be an integer")
    return get_or_create_chat(db=db, customer_id=user_id, shop_id=shop_id)


@router.post("/send_message", response_model=MessageSchema)
def send_message(user_id: UserDep, db: dbDep, message: CustomerMessageCreateSchema):
    message = create_message(db, customer_id=user_id, shop_id=message.shop_id, message_body=message.body)
    return message


@router.get("/chat/{shop_id}")
def get_chat(user_id: UserDep, db: dbDep, shop_id: int):
    return get_messages(db=db, customer_id=user_id, shop_id=shop_id)


@router.get("/chats", response_model=list[ChatModelSchema])
def get_customer_chats(user_id: UserDep, db: dbDep):
    return get_chats_by_customer_id(db, user_id)

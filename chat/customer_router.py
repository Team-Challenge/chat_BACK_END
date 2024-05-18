from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from chat.core.dependencies import UserDep
from chat.database.crud import (get_or_create_chat, create_message, get_messages,
                                get_chats_by_customer_id)
from chat.database.database import dbDep
from chat.database.schemas import MessageSchema, CustomerMessageCreateSchema, ChatsSchema, ChatModelSchema

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.post("/create_chat")
def create_chat(user: UserDep, db: dbDep, shop_owner_id):
    return get_or_create_chat(db=db, customer_id=user.id, shop_owner_id=shop_owner_id)


@router.post("/send_message", response_model=MessageSchema)
def send_message(user: UserDep, db: dbDep, message: CustomerMessageCreateSchema):
    message = create_message(db, customer_id=user.id, shop_owner_id=message.shop_owner_id, message_body=message.body)
    return message


@router.get("/chat/{shop_owner_id}")
def get_chat(user: UserDep, db: dbDep, shop_owner_id: int):
    return get_messages(db=db, customer_id=user.id, shop_owner_id=shop_owner_id)


@router.get("/chats", response_model=list[ChatModelSchema])
def get_customer_chats(user: UserDep, db: dbDep):
    return get_chats_by_customer_id(db, user.id)

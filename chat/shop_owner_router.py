from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from chat.core.dependencies import UserDep
from chat.core.exceptions import ChatCreationError
from chat.database.crud import create_message, get_messages, \
    get_chats_by_shop_owner_id
from chat.database.database import dbDep
from chat.database.schemas import MessageSchema, ShopOwnerMessageCreateSchema, ChatsSchema, \
    ChatSchema

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/shop_owner", tags=["Shop owner"])


@router.post("/send_message", response_model=MessageSchema)
def send_message(user: UserDep, db: dbDep, message: ShopOwnerMessageCreateSchema):
    message = create_message(db, customer_id=message.customer_id, shop_owner_id=user.id, message_body=message.body)
    return message


@router.get("/chat/{customer_id}", response_model=ChatSchema)
def get_chat(user: UserDep, db: dbDep, customer_id: int):
    return get_messages(db, customer_id=customer_id, shop_owner_id=user.id)


@router.get("/chats", response_model=ChatsSchema, responses={400: ChatCreationError.desc()})
def get_shop_owner_chats(user: UserDep, db: dbDep):
    chats = get_chats_by_shop_owner_id(db, user.id)
    return ChatsSchema(chats=chats)

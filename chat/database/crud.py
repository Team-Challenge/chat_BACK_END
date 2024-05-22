from sqlalchemy.orm import Session

from chat.core.dependencies import check_shop_id
from chat.core.exceptions import ChatCreationError
from chat.database.models import Message, Chat
from chat.database.schemas import ChatSchema


def get_or_create_chat(db: Session, customer_id: int, shop_id: int):
    shop_owner = check_shop_id(shop_id)
    if customer_id == shop_owner:
        return ChatCreationError
    room = db.query(Chat).filter_by(customer_id=customer_id, shop_id=shop_id).first()
    if not room:
        room = Chat(customer_id=customer_id, shop_id=shop_id)
        db.add(room)
        db.commit()
        db.refresh(room)
    return room


def create_message(db: Session, customer_id: int, shop_id: int, message_body: str):
    chat = get_or_create_chat(db, customer_id=customer_id, shop_id=shop_id)
    message = Message(chat_id=chat.id,
                      owner_id=customer_id,
                      body=message_body)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, customer_id: int, shop_id: int, skip: int = 0, limit: int = 100):
    chat = get_or_create_chat(db, customer_id=customer_id, shop_id=shop_id)
    messages = db.query(Message).where(Message.chat_id == chat.id, Message.deleted_at == None).offset(skip).limit(
        limit).all()

    return ChatSchema(**chat.__dict__, messages=messages)


def get_message_by_id(db: Session, message_id: int) -> Message:
    return db.query(Message).get(message_id)


def get_chats_by_customer_id(db: Session, user_id: int) -> list[Chat]:
    return db.query(Chat).where(Chat.customer_id == user_id).all()


def get_chats_by_shop_owner_id(db: Session, user_id: int) -> list[Chat]:
    return db.query(Chat).where(Chat.shop_id == user_id).all()


def soft_delete_message(db: Session, user_id, message_id: int):
    message = get_message_by_id(db, message_id)
    if message and message.owner_id == user_id:
        message.delete()
        db.commit()
        return {"message": "Message deleted"}
    return {"message": "Message not found"}

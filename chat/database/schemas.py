from typing import Optional

from pydantic import BaseModel, ConfigDict


class CustomerMessageCreateSchema(BaseModel):
    shop_id: int
    body: str

    model_config = ConfigDict(from_attributes=True)


class ShopOwnerMessageCreateSchema(BaseModel):
    customer_id: int
    body: str

    model_config = ConfigDict(from_attributes=True)


class MessageSchema(BaseModel):
    id: int
    chat_id: int
    owner_id: int
    body: str

    model_config = ConfigDict(from_attributes=True)


class ChatSchema(BaseModel):
    id: int
    customer_id: int
    shop_id: int
    messages: list[MessageSchema] = []

    model_config = ConfigDict(from_attributes=True)


class ChatModelSchema(BaseModel):
    id: int
    customer_id: int
    shop_id: int
    last_message: Optional[MessageSchema] = None
    model_config = ConfigDict(from_attributes=True)


class ChatsSchema(BaseModel):
    chats: list[ChatModelSchema]

    model_config = ConfigDict(from_attributes=True)

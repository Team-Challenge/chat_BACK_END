from typing import Optional

from pydantic import BaseModel, ConfigDict


class CustomerMessageCreateSchema(BaseModel):
    shop_owner_id: int
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
    is_shop_owner: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
    # @field_validator("is_shop_owner",mode="after")
    # @classmethod
    # def check_owner(cls):


class ChatSchema(BaseModel):
    id: int
    customer_id: int
    shop_owner_id: int
    messages: list[MessageSchema] = []

    model_config = ConfigDict(from_attributes=True)


class ChatModelSchema(BaseModel):
    id: int
    customer_id: int
    shop_owner_id: int
    last_message: Optional[MessageSchema] = None
    model_config = ConfigDict(from_attributes=True)


class ChatsSchema(BaseModel):
    chats: list[ChatModelSchema]

    model_config = ConfigDict(from_attributes=True)


class UserCopy(BaseModel):
    id: int
    email: str
    full_name: str
    profile_picture: str | None = None
    phone_number: str | None = None
    shop_id: int | None = None

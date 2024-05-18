from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped, object_session, mapped_column

from chat.database.database import Base
from chat.database.schemas import UserCopy


class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

    def delete(self):
        self.deleted_at = datetime.now()

    def undelete(self):
        self.deleted_at = None


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    profile_picture = Column(String)
    phone_number = Column(String)
    shop_id = Column(Integer)

    last_check = Column(DateTime, nullable=True, default=datetime.now)

    messages = relationship("Message", back_populates="owner")

    def update(self, user: UserCopy):
        self.email = user.email
        self.full_name = user.full_name
        self.profile_picture = user.profile_picture
        self.phone_number = user.phone_number
        self.shop_id = user.shop_id
        self.last_check = datetime.now()
        return self


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    shop_owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    customer = relationship("User", foreign_keys=[customer_id])
    shop_owner = relationship("User", foreign_keys=[shop_owner_id])

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    # @hybrid_method
    # def last_message(self, db: dbDep):
    #     msg = db.query(Message).where(Message.chat_id == self.id).order_by(Message.created_at).first()
    #     print(msg)
    #     return msg

    @hybrid_property
    def last_message(self):
        return object_session(self).query(Message).where(Message.chat_id == self.id).order_by(Message.id.desc()).first()


class Message(Base, SoftDeleteMixin):
    __tablename__ = "message"
    # id = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('Chat', back_populates='messages')
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="messages")

    body = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    @hybrid_property
    def is_shop_owner(self):
        if self.chat.shop_owner_id == self.owner_id:
            return True
        return False

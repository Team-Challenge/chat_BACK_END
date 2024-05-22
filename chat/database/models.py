from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from chat.database.database import Base


class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

    def delete(self):
        self.deleted_at = datetime.now()

    def undelete(self):
        self.deleted_at = None


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    shop_id = Column(Integer, nullable=False)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


class Message(Base, SoftDeleteMixin):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('Chat', back_populates='messages')
    owner_id = Column(Integer, nullable=False)

    body = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

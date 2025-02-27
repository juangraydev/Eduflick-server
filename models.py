from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    flash_card = relationship("FlashCards", back_populates="user", uselist=False)

class FlashCards(Base):
    __tablename__ = 'flash_cards'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="flash_card")
    cards = relationship("Cards", back_populates="flash_card")

class Cards(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(100))
    answer = Column(String(100))
    flash_card_id = Column(Integer, ForeignKey('flash_cards.id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    flash_card = relationship("FlashCards", back_populates="cards")
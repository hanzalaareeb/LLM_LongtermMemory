import os
from datetime import datetime
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship
from base import Base
from db import User

DATABASE_URL = "sqlite:///./conversationturn.db"

engine = create_engine(DATABASE_URL, echo=False) #TODO echo=False
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ConversationTurn(Base):
    """Model to create a single pair of a user input and bot output."""
    __tablename__ = "conversation_turn"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    message_date_local = Column(Date, nullable=False)
    message = Column(Text, nullable=False)
    answered_at = Column(DateTime, nullable=True)
    answer = Column(Text, nullable=False)
    character = Column(String(25), nullable=False)
    
    user = relationship("User", back_populates="conversation_turns")

    DATE_FORMAT = '%B %dth %Y'

    def __str__(self):
        return f'id: {self.id} user_message: {self.message}'

    def message_with_date(self):
        formatted_local_date = self.message_date_local.strftime(self.DATE_FORMAT)
        return f'[{formatted_local_date}] {self.message}'

    def answer_with_date(self):
        formatted_local_date = self.message_date_local.strftime(self.DATE_FORMAT)
        return f'[{formatted_local_date}] {self.answer}'

    def convert_to_string(self):
        local_date_str = self.message_date_local.strftime(self.DATE_FORMAT)
        return f'[{local_date_str}] {self.user.name}: {self.message}\n[{local_date_str}] {self.character}: {self.answer}\n'

# Add back_populates to User model. Why am I doing this? 
User.conversation_turns = relationship("ConversationTurn", back_populates="user")

if __name__ == "__main__":
    logging.info("satrtttttttttt...")
    Base.metadata.drop_all(bind=engine)  # Be cautious with this in production
    Base.metadata.create_all(bind=engine)
    logging.info("suck")

import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import logging
from base import Base  

logging.basicConfig(level=logging.INFO)

def get_conversation_turn():
    from converturn_db import ConversationTurn
    return ConversationTurn

DATABASE_URL = "sqlite:///./memory.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    memories = relationship("Memory", back_populates="user")
    
    # This relationship should point to the ConversationTurn model once defined
    conversation_turns = relationship("ConversationTurn", back_populates="user") 

class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    core_memory = Column(Text)
    user_info_memory = Column(Text)
    other_memory = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="memories")



def init_db():
    logging.info("Init db...")
    Base.metadata.create_all(bind=engine)
    logging.info("hurrahhhhh asshole!")

if __name__ == "__main__":
    init_db()
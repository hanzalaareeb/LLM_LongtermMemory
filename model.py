"""
model.py
---------
Single file containing all models (User, Memory, ConversationTurn)
and a single database engine pointing to app.db.
"""

import datetime
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


# Set up logging
logging.basicConfig(level=logging.INFO)

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    memories = relationship("Memory", back_populates="user")
    conversation_turns = relationship("ConversationTurn", back_populates="user")

    def __repr__(self):
        return f"User id={self.id}, name={self.name}"


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    core_memory = Column(Text)
    user_info_memory = Column(Text)
    other_memory = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship back to User
    user = relationship("User", back_populates="memories")

    def __repr__(self):
        return f"Memory id={self.id}, user_id={self.user_id}"


class ConversationTurn(Base):
    __tablename__ = "conversation_turn"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_date_local = Column(Date, nullable=False)
    message = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    character = Column(String(25), nullable=False)

    # Relationship back to User
    user = relationship("User", back_populates="conversation_turns")

    DATE_FORMAT = '%B %dth %Y'

    def __str__(self):
        return f"id: {self.id} user_message: {self.message}"

    def message_with_date(self):
        formatted_local_date = self.message_date_local.strftime(self.DATE_FORMAT)
        return f"[{formatted_local_date}] {self.message}"

    def answer_with_date(self):
        formatted_local_date = self.message_date_local.strftime(self.DATE_FORMAT)
        return f"[{formatted_local_date}] {self.answer}"

    def convert_to_string(self):
        local_date_str = self.message_date_local.strftime(self.DATE_FORMAT)
        return (
            f"[{local_date_str}] {self.user.name}: {self.message}\n"
            f"[{local_date_str}] {self.character}: {self.answer}\n"
        )

# --- Initialization Function ---
def init_db():
    """
    Creates all tables in the database in single memory.db file.
    """
    logging.info("start...")
    Base.metadata.create_all(bind=engine)
    logging.info("end...")



if __name__ == "__main__":
    init_db()

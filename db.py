import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DATABASE_URL = "sqlite:///./memory.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    memories = relationship("Memory", back_populates="user")
# memory class
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
    print("Init db...")
    Base.metadata.create_all(bind=engine)
    print("hurrahhhhh asshole!")

if __name__ == "__main__":
    init_db()
from sqlalchemy.orm import (
  DeclarativeBase,
  sessionmaker
)
from sqlalchemy import Column, String, DateTime, func, create_engine, Integer

DATABASE_URL = "sqlite:///task_manager.db"

class Base(DeclarativeBase):
  pass

class Tasks(Base):
  __tablename__="tasks"
  id = Column(Integer, primary_key=True)
  title = Column(String)
  description = Column(String)
  status = Column(String)
  created_at = Column(DateTime(timezone=True), default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

import os

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Enum, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

from sqlalchemy.orm import sessionmaker

load_dotenv()

Base = declarative_base()


class StatusEnum(enum.Enum):
    alive = "alive"
    dead = "dead"
    finished = "finished"


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(StatusEnum), default=StatusEnum.alive)
    status_updated_at = Column(DateTime, default=datetime.utcnow)


engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

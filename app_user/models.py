from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Enum, BigInteger
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

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

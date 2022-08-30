from libraries.database.db import Base
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime, BigInteger


class Member(Base):
    __tablename__ = "Member"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(20))
    desc = Column(Integer)
    points = Column(Integer)
    update_time = Column(DateTime)
    status = Column(String(20))

    def __init__(self, user_id, name, desc, points, update_time, status):
        self.id = user_id
        self.name = name
        self.desc = desc
        self.points = points
        self.update_time = update_time
        self.status = status


# TODO: add Base also think of options column like relationship to other


class Bet:
    __tablename__ = "Bet"
    id = Column(index=True)
    title = Column()
    options = Column()

    def __init__(self, title, options: list):
        self.title = title
        self.options = options


class Options:
    __tablename__ = "Options"

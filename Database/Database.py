from sqlalchemy import create_engine, DateTime, func, Boolean, Float, PickleType, desc
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    win = Column(Integer)
    loss = Column(Integer)

    def __init__(self, d_id):
        self.discord_id = d_id
        self.win = 0
        self.loss = 0


class UserHandler:
    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine('sqlite:///db.db', echo=False)
        Base.metadata.create_all(self.engine)

    def check_user(self, d_id):
        session = sessionmaker(bind=self.engine)()
        flag = True

        lst = session.query(User).filter(User.discord_id == d_id).first()
        if lst is None:
            flag = False

        return flag

    def add_user(self, d_id):
        session = sessionmaker(bind=self.engine)()

        user = User(d_id)

        lst = session.query(User).filter(User.discord_id == d_id).first()
        if lst is None:
            session.add(user)
            session.commit()
            return True

        session.close()
        return False

    def get_profile(self, d_id):
        session = sessionmaker(bind=self.engine)()
        user = session.query(User).filter(User.discord_id == d_id).first()
        ret = [user.win, user.loss]
        session.close()
        return ret

    def get_game(self, d_id, result):
        session = sessionmaker(bind=self.engine)()
        user = session.query(User).filter(User.discord_id == d_id).first()
        if result == 0:
            user.loss += 1
        else:
            user.win += 1
        session.commit()
        session.close()
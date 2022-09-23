from sqlalchemy import create_engine, DateTime, func, Boolean, Float, PickleType, desc
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query

Base = declarative_base()


class Server(Base):
    __tablename__ = 'Servers'
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    name = Column(String)
    last_day = Column(String)
    daly_channel = Column(Integer)

    def __init__(self, d_id, name):
        self.discord_id = d_id
        self.name = name
        self.last_day = None
        self.daly_channel = None


class ServerHandler:
    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine('sqlite:///db.db', echo=False)
        Base.metadata.create_all(self.engine)

    def get_last_day(self, d_id):
        session = sessionmaker(bind=self.engine)()

        lst = session.query(Server).filter(Server.discord_id == d_id).first()
        if lst is None:
            flag = False

        return lst.last_day

    def get_servers(self):
        session = sessionmaker(bind=self.engine)()
        return session.query(Server).all()

    def set_daly_channel(self, d_id, c_id):
        session = sessionmaker(bind=self.engine)()

        lst = session.query(Server).filter(Server.discord_id == d_id).first()

        lst.daly_channel = c_id
        session.commit()
        session.close()

    def set_day(self, d_id, day):
        session = sessionmaker(bind=self.engine)()

        lst = session.query(Server).filter(Server.discord_id == d_id).first()

        lst.last_day = day
        session.commit()
        session.close()

    def add_server(self, d_id, name):
        session = sessionmaker(bind=self.engine)()

        srv = Server(d_id, name)

        lst = session.query(Server).filter(Server.discord_id == d_id).first()
        if lst is None:
            session.add(srv)
            session.commit()
            return True

        session.close()
        return False

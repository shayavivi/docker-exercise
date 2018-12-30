import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ClientData(Base):  # row in the DB
    __tablename__ = 'client_data'  # table name

    id = Column(Integer, primary_key=True)
    rawData = Column(String)
    result = Column(Integer, default=None)

    @classmethod
    def create_from_json(cls, json_data):
        """
        json example:
        {
            1: "2,3,4,5"
            2: "11,6,10,5"
            3: "7,3,21,5"
            4: "9,2,1,16"
        }
        """
        session = Session()

        for row_id in json_data:
            datarow = cls(id=int(row_id), rawData=str(json_data[row_id]))
            session.add(datarow)

        session.commit()  # commit all changes to DB
        session.close()

    @classmethod
    def get_result(cls, req_id):
        session = Session()
        result = session.query(cls).get(req_id)  # filter the rows in db by id
        session.close()
        return result


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///tasks.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)  # create DB
Session = sessionmaker(bind=engine)


def create():
    Base.metadata.create_all(bind=engine)


if SQLALCHEMY_DATABASE_URI == 'sqlite:///tasks.db':
    if not os.path.exists("tasks.db"):
        create()
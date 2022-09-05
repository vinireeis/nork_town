# Standards
import sqlalchemy
from sqlalchemy.orm import Session


from decouple import config


class SqliteInfrastructure:

    connection = None
    session = None

    @classmethod
    def __get_connection(cls):
        if cls.connection is None:
            engine = sqlalchemy.create_engine(config("HOST_URL"))
            cls.connection = engine.connect()
        return cls.connection

    @classmethod
    def get_session(cls):
        if cls.session is None:
            engine = sqlalchemy.create_engine(config("HOST_URL"))
            cls.session = Session(engine)
        return cls.session

    @classmethod
    def script_create_client_table(cls):
        sql_script = """CREATE TABLE IF NOT EXISTS CLIENT(
                        ID INTEGER PRIMARY KEY,
                        EMAIL VARCHAR (60),
                        NAME VARCHAR (50),
                        SALE_OPPORTUNITY INT)
                   """
        connection = cls.__get_connection()
        connection.execute(sql_script)

    @classmethod
    def script_create_car_table(cls):
        sql_script = """CREATE TABLE IF NOT EXISTS CAR(
                        ID INTEGER PRIMARY KEY,
                        MODEL VARCHAR (11),
                        COLOR VARCHAR (10),
                        CLIENT_ID INTEGER)
                   """
        connection = cls.__get_connection()
        connection.execute(sql_script)

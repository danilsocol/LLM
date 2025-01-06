from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel, Session, create_engine
from database.config import get_settings


engine = create_engine(url=get_settings().DATABASE_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    print("New Database Created" + database_exists(engine.url))
else:
    print("Database Already Exists")

def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)



import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from libraries import CONFIG

engine = db.create_engine(
    f"mysql+mysqlconnector://" f"{CONFIG.Database.Login}:" f"{CONFIG.Database.Password}@localhost:3306/discord"
)
if not database_exists(engine.url):
    print("Creating database..")
    create_database(engine.url)


print("Database existence:", database_exists(engine.url))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database_session():
    try:
        Base.metadata.create_all(bind=engine)
        database = SessionLocal()
        return database
    finally:
        database.close()

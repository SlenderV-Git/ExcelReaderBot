from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect, text

from src.database.models.models import Base

def get_session(reflesh : bool = False):
    engine = create_engine('sqlite:///mydatabase.db')
    session = sessionmaker(bind=engine)()
    if reflesh:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        for table_name in table_names:
            if table_name != "manager":
                session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        session.commit()
    Base.metadata.create_all(engine)
    return session
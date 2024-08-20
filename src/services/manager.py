from src.database.models.models import Manager
from aiogram.types import Message
from sqlalchemy import select, delete
from src.database.gateway import get_session

def add_manager(manager_id : str, full_name : str, session = get_session()):
    manager = Manager(manager_id= manager_id, manager_fullname = full_name)
    session.add(manager)
    session.commit()
    
def delete_manager(manager_id : str, session = get_session()):
    stmt = delete(Manager).where(Manager.manager_id == manager_id)
    session.execute(stmt)
    session.commit()

def list_managers(session = get_session()):
    stmt = select(Manager)
    return session.execute(stmt).scalars().all()

def list_id_managers(session = get_session()):
    stmt = select(Manager.manager_id)
    return session.execute(stmt).scalars().all()
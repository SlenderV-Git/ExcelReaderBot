from aiogram.fsm.state import State, StatesGroup

class DocumentTracker(StatesGroup):
    get_document = State()

class InnTracker(StatesGroup):
    get_inn = State()
    
class PartName(StatesGroup):
    get_part_name = State()
    
class AddManager(StatesGroup):
    get_manager_id = State()
    get_manager_name = State()
    
class DeleteManager(StatesGroup):
    get_manager_id = State()


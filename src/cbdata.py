from aiogram.filters.callback_data import CallbackData


class AdminMenuCallbackFactory(CallbackData, prefix='admin'):
    action : str
    
class PaginationCallbackFacory(CallbackData, prefix= "pag"):
    type_pagination : str
    data : int | str
    offset : int
    
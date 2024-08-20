from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from src.core.settings import get_settings

from src.keyboards.kb_admin import get_start_kb, get_pagination_kb
from src.cbdata import AdminMenuCallbackFactory, PaginationCallbackFacory
from src.state import DocumentTracker, InnTracker, PartName, AddManager, DeleteManager
from src.services.bd_search import (get_products_by_inn, 
                                    get_consignee_by_inn, 
                                    get_last_product_cost, 
                                    get_product_orders,
                                    get_products_by_partname,
                                    get_consignee_by_order)
from src.services.manager import add_manager, delete_manager, list_managers, list_id_managers
from src.dialogs.ru_dialogs import *
from ...keyboards.kb_admin import TEST

rt = Router()
 
@rt.callback_query(AdminMenuCallbackFactory.filter())
async def admin_menu_process(callback : CallbackQuery, callback_data : AdminMenuCallbackFactory, state : FSMContext):
    if  callback_data.action == "send_doc" and (TEST or callback.from_user.id in get_settings().ADMIN_ID):
        await state.set_state(DocumentTracker.get_document)
        await callback.answer()
        await callback.message.answer(REQUEST_DOC)
    elif callback_data.action == "send_inn":
        await state.set_state(InnTracker.get_inn)
        await callback.answer()
        await callback.message.answer(REQUEST_INN)
    elif callback_data.action == "part_name":
        await state.set_state(PartName.get_part_name)
        await callback.answer()
        await callback.message.answer(REQUEST_PART_NAME)
        
    elif callback_data.action == "add_manager" and (TEST or callback.from_user.id in get_settings().ADMIN_ID):
        await state.set_state(AddManager.get_manager_id)
        await callback.answer()
        await callback.message.answer(REQUEST_MANAGER_ID)
    
    elif callback_data.action == "delete_manager" and (TEST or callback.from_user.id in get_settings().ADMIN_ID):
        await state.set_state(DeleteManager.get_manager_id)
        await callback.answer()
        await callback.message.answer(REQUEST_MANAGER_ID)
    
    elif callback_data.action == "list_manager" and (TEST or callback.from_user.id in get_settings().ADMIN_ID):
        await callback.answer()
        await callback.message.answer("\n".join(map(lambda x: str(x), list_managers())))
        
@rt.message(StateFilter(AddManager.get_manager_id))
async def add_manager_process(message : Message, state : FSMContext):
    if len(message.text) == 10 and message.text.isdigit():
        await state.set_data({"user" : int(message.text)})
        await message.answer("Теперь укажите имя менеджера")
        await state.set_state(AddManager.get_manager_name)
    else:
        await message.answer("Айди пользователя должен состоять из цифр и быть длинной в 10 символов")
        await state.clear()
        
@rt.message(StateFilter(AddManager.get_manager_name))
async def add_manager_name_process(message : Message, state : FSMContext):
    try:
        manager_data = await state.get_data()
        print(manager_data.get("user")in list_id_managers()) 
        add_manager(manager_id=manager_data.get("user"), full_name=message.text)
        await message.answer("Операция успешно проведена")
    except Exception as e:
        print(e)
        await message.answer("Менеджер уже существует")
    await state.clear()
    
@rt.message(StateFilter(DeleteManager.get_manager_id))
async def delete_manager_process(message : Message, state : FSMContext):
    await state.clear()
    try:
        if len(message.text) == 10 and message.text.isdigit():
            delete_manager(manager_id=int(message.text))
            await message.answer("Операция успешно проведена")
        else:
            await message.answer("Айди пользователя должен состоять из цифр и быть длинной в 10 символов")
    except Exception as e:
        print(e)
        await message.answer("Менеджера нет в базе данных")
        
@rt.message(StateFilter(InnTracker.get_inn))
async def inn_seach_process(message : Message, state : FSMContext):
    if message.text.isdigit():
        product = get_products_by_inn(message.text)
        consegnee = get_consignee_by_inn(message.text)
        if product:
            last_price = get_last_product_cost(product[0].id)
            await message.answer(text = f'Грузополучатель: {consegnee.name}\n\n{consegnee.inn}\n{product[0]}.\n\nПоследняя цена: {last_price} руб.', 
                                 reply_markup= get_pagination_kb("inn", 
                                                                 data= message.text, 
                                                                 pag_len=len(product),
                                                                 id=product[0].id))
            await state.clear()
        else:
            await message.answer("Ничего не найдено")
    else:
        await message.answer("ИНН должен полность состоять из цифр")

@rt.callback_query(PaginationCallbackFacory.filter())
async def admin_menu_process(callback : CallbackQuery, callback_data : PaginationCallbackFacory, state : FSMContext):
    if callback_data.type_pagination == "inn":
        product = get_products_by_inn(callback_data.data, callback_data.offset)
        consegnee = get_consignee_by_inn(callback_data.data)
        last_price = get_last_product_cost(product[0].id)
        await callback.message.edit_text(text = f'Грузополучатель: {consegnee.name}\n\n{consegnee.inn}\n{product[0]}.\n\nПоследняя цена: {last_price} руб.', 
                                         reply_markup= get_pagination_kb("inn", 
                                                                        data=callback_data.data, 
                                                                        pag_len=len(product),
                                                                        id = product[0].id,
                                                                        offset=callback_data.offset)
                                         )
    elif callback_data.type_pagination in ["inn_select", "part_name_pag_select"]:
        consegnee = get_consignee_by_order(callback_data.data)
        orders = get_product_orders(callback_data.data)
        if orders and consegnee:
            order_data = "\n".join(map(lambda x : str(x), orders))
            await callback.message.answer(f"{consegnee.name} {consegnee.inn}\n{order_data}")
        else:
            await callback.message.answer("По указанному продукту не найдено заказов")
            
    elif callback_data.type_pagination == "part_name_pag":
        products = get_products_by_partname(callback_data.data, offset= callback_data.offset)
        if products:
            last_price = get_last_product_cost(products[0].id)
            await callback.message.edit_text(text= f"{products[0]}. Последняя цена: {last_price} руб.", reply_markup=get_pagination_kb("part_name_pag",
                                                                                data=callback_data.data,
                                                                                pag_len=len(products),
                                                                                id=products[0].id,
                                                                                offset=callback_data.offset
                                                                                ))

@rt.message(StateFilter(PartName.get_part_name))
async def search_process(message : Message, state : FSMContext):
    products = get_products_by_partname(message.text)
    await state.clear()
    if products:
        last_price = get_last_product_cost(products[0].id)
        await message.answer(text= f"{products[0]}. Последняя цена: {last_price} руб.", reply_markup=get_pagination_kb("part_name_pag",
                                                                                data=message.text,
                                                                                pag_len=len(products) + 1,
                                                                                id=products[0].id
                                                                                )
                             )
    else:
        await message.answer("Ничего не найдено")
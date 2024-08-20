from src.models.excel_objects import Consignee, Product, Order, TypeProduct
from pandas import read_excel, DataFrame
from math import isnan
from io import BytesIO

def string_filter(string : list[str], row):
    return all(list(map(lambda x: x not in "".join(map(lambda x : str(x), row.to_list())), string)))


def read_all_pages(file : BytesIO):
    result = []
    sheets = read_excel(file, sheet_name=None, header=None)
    for sheet in sheets.values():
        data = process_excel(sheet)
        result.extend(data)
    return result
    
def process_excel(df : DataFrame):
    consignees = {}
    current_consignee = None
    current_product = None
    current_type = None
    
    for index, row in df.iterrows():
        if 'ГРУЗОПОЛУЧАТЕЛЬ' in "".join(map(lambda x : str(x), row.to_list())):
            data = row.to_list()[0]
            name_index = data.find("Наименование")
            inn_index = data.find("ИНН")
            kpp_index = data.find("КПП")
            adress_index = data.find("Адрес")
            
            current_consignee = Consignee(
                name= data[name_index : inn_index -2],
                inn= data[inn_index : kpp_index -2],
                kpp= data[kpp_index : adress_index -2],
                adress= data[adress_index :],
                type_products=[])
            consignees[data[name_index : inn_index + 1]] = current_consignee
            
        elif 'Вид продукции' in "".join(map(lambda x : str(x), row.to_list())) and current_consignee:
            product_type = row.to_list()[0]
            current_type = TypeProduct(product_type, products= [])
            current_consignee.type_products.append(current_type)
            
        elif current_product and current_consignee and isinstance(row.to_list()[0], int) and current_product:
            row_list = row.to_list()
            if not isinstance(row_list[3], (str, int)):
                row_list.pop(3)
            if len(row_list) > 10 and not isinstance(row_list[10], (str, int)):
                row_list.pop(10)
            row_data = list(map(lambda x : None if isinstance(x, float) and isnan(x) else x, row_list))
            order = Order(*row_data)
            current_product.orders.append(order)
        
        elif current_type and string_filter(["Всего по наименованию продукции:", "Всего по виду продукции:", "Итого по организации – грузополучателю:"], row):
            row_data = row.to_list()
            current_product = Product(
                product_name= row_data[0],
                quantity=None,
                cost= None,
                orders= []
            )
            current_type.products.append(current_product)
    return list(consignees.values())
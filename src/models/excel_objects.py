class Order:
    def __init__(self, order_id, number, date, date_fix, status, number_ttn, time_fix, cost, date_import, quantity, total_cost):
        self.order_id = order_id
        self.number = number
        self.date = date
        self.date_fix =  date_fix
        self.status = status
        self.number_ttn = number_ttn
        self.time_fix = time_fix
        self.cost = cost
        self.date_import = date_import
        self.quantity = quantity
        self.total_cost = total_cost
    
    def __str__(self) -> str:
        return f"Данные заказа: {' '.join(map(lambda x: str(x), self.__dict__.values()))}"
        
class TypeProduct:
    def __init__(self, product_type, products):
        self.product_type = product_type
        self.products = products
    
    def __str__(self) -> str:
        products = '\n'.join(map(lambda x: str(x), self.products))
        return f"Tип продукта: {self.product_type}, Продукты:\n{products}"

class Product:
    def __init__(self, product_name, quantity, cost, orders) -> None:
        self.product_name = product_name
        self.quantity = quantity
        self.cost = cost
        self.orders = orders
        
    def __str__(self) -> str:
        orders = '\n'.join(map(lambda x: str(x), self.orders))
        return f"Имя продукта: {self.product_name}, Заказы:\n{orders}"
    
class Consignee:
    def __init__(self, name, inn, kpp, adress, type_products):
        self.name = name
        self.inn = inn
        self.kpp = kpp
        self.adress = adress
        self.type_products = type_products
        
    def __str__(self) -> str:
        types = '\n'.join(map(lambda x: str(x), self.type_products))
        return f"Грузополучатель {self.name}, ИНН: {self.inn}, Типы продуктов:\n{types}"
from src.database.models.models import Consignee, TypeProduct, Product, Order
from io import BytesIO
from src.services.excel import read_all_pages
from src.database.gateway import get_session

def convert_and_add_to_session(consignee_obj, session):
    consignee = Consignee(
        name=consignee_obj.name, 
        inn = consignee_obj.inn,
        kpp = consignee_obj.kpp,
        adress = consignee_obj.adress
        )
    session.add(consignee)
    for type_product_obj in consignee_obj.type_products:
        type_product = TypeProduct(product_type=type_product_obj.product_type, consignee=consignee)
        session.add(type_product)
        for product_obj in type_product_obj.products:
            product = Product(
                product_name=product_obj.product_name,
                quantity=product_obj.quantity,
                cost=product_obj.cost,
                type_product=type_product
            )
            session.add(product)
            for order_obj in product_obj.orders:
                try:
                    total_cost = float(order_obj.total_cost)
                except:
                    total_cost = 0
                order = Order(
                    order_id=order_obj.order_id,
                    number=order_obj.number,
                    date=str(order_obj.date),
                    date_fix=str(order_obj.date_fix),
                    status=order_obj.status,
                    number_ttn=order_obj.number_ttn,
                    time_fix=str(order_obj.time_fix),
                    cost=order_obj.cost,
                    date_import=str(order_obj.date_import),
                    quantity=order_obj.quantity,
                    total_cost=total_cost,
                    product=product
                )
                session.add(order)
    session.commit()
    
def convert_file_to_db(file : BytesIO):
    data = read_all_pages(file)
    session = get_session(reflesh=True)
    
    for obj in data:
        try:
            convert_and_add_to_session(obj, session=session)
        except Exception as e:
            print(e)
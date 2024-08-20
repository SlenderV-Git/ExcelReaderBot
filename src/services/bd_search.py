from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from fuzzywuzzy import process
from src.database.models.models import Consignee, Product, Order, TypeProduct
from src.database.gateway import get_session

def get_products_by_inn(inn, offset = 0, session = get_session()):
    result = session.query(Product).\
        join(TypeProduct, TypeProduct.id == Product.type_product_id).\
        join(Consignee, Consignee.id == TypeProduct.consignee_id).\
        filter(Consignee.inn.like(f"%{inn}%")).offset(offset).all()
    return result

def get_consignee_by_inn(inn, session = get_session()):
    stmt = select(Consignee).where(Consignee.inn.like(f"%{inn}%"))
    return session.execute(stmt).scalars().first()

def get_product_orders(product_id, session = get_session()):
    stmt = (select(Order)
            .join(Product, Product.id == Order.product_id)
            .where(Product.id == product_id)
            .order_by(Order.date.desc()))
    return session.execute(stmt).scalars().all()
    

def get_last_product_cost(id : str | int, session = get_session()):
    stmt = select(Order).join(Product, Product.id == Order.product_id).filter(Product.id == id).order_by(Order.date.desc())
    return session.execute(stmt).scalars().first().cost

def get_products_by_partname(partname : str, offset : str = 0, session = get_session()):
    products = session.query(Product).all()
    product_names = [product.product_name for product in products]
    matches = process.extract(partname.lower(), product_names, limit=3)
    matched_products = [product for product in products if product.product_name in dict(matches).keys()]
    if offset > len(matched_products) -1:
        offset = len(matched_products) -1
    return matched_products[offset :]

def get_consignee_by_order(order_id: int, session = get_session()):
    consignee = session.query(Consignee).\
        join(TypeProduct, Consignee.id == TypeProduct.consignee_id).\
        join(Product, TypeProduct.id == Product.type_product_id).\
        join(Order, Product.id == Order.product_id).\
        filter(Order.id == order_id).\
        first()
    return consignee
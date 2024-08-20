from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Consignee(Base):
    __tablename__ = 'consignees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    inn = Column(String)
    kpp =  Column(String)
    adress = Column(String)

    type_products = relationship('TypeProduct', back_populates='consignee')

class TypeProduct(Base):
    __tablename__ = 'type_products'
    id = Column(Integer, primary_key=True)
    product_type = Column(String, nullable=False)
    consignee_id = Column(Integer, ForeignKey('consignees.id'))

    consignee = relationship('Consignee', back_populates='type_products')
    products = relationship('Product', back_populates='type_product')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
    cost = Column(Float, nullable = True)
    type_product_id = Column(Integer, ForeignKey('type_products.id'))

    type_product = relationship('TypeProduct', back_populates='products')
    orders = relationship('Order', back_populates='product')
    
    def __str__(self):
        return " ".join(filter(lambda x : x , [self.product_name, self.quantity, self.cost]))

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=True)
    number = Column(String, nullable=True)
    date = Column(String, nullable=True)
    date_fix = Column(String)
    status = Column(String, nullable=True)
    number_ttn = Column(String)
    time_fix = Column(String)
    cost = Column(Float, nullable=True)
    date_import = Column(String)
    quantity = Column(Integer, nullable=True)
    total_cost = Column(Float, nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship('Product', back_populates='orders')
    
    def __str__(self):
        return f"Дата: {self.date}\nСтоимость: {self.cost} руб.\n"
    
class Manager(Base):
    __tablename__ = "manager"
    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, nullable = False, unique=True)
    manager_fullname = Column(String, nullable=True)
    
    def __str__(self):
        return f"{self.id}) {self.manager_fullname} - id {self.manager_id}"
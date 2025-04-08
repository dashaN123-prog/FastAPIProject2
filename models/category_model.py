from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import base


class Category(base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    products_list = relationship('Product', back_populates='categories', uselist=True)


class Product(base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    description = Column(String(255), nullable=False)
    img_url = Column(String(255), nullable=False)
    age_restriction = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('category.id'))

    categories = relationship('Category', back_populates='products_list', uselist=False)

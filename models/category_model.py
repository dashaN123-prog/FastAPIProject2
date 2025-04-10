from sqlalchemy import Column, Integer, String, ForeignKey, Float
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
    cart_products = relationship('CartProduct', back_populates='product')


class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    tg_id = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    id_role = Column(Integer, ForeignKey('roles.id'), nullable=False)

    cart = relationship('Cart', back_populates='user', uselist=False, cascade="all, delete-orphan")
    bonus_card = relationship('BonusCard', back_populates='userId', uselist=False, cascade="all, delete-orphan")
    roles = relationship('Role', back_populates='users_list', uselist=False)


class Cart(base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='cart')
    cart_products = relationship('CartProduct', back_populates='cart', cascade="all, delete-orphan")


class CartProduct(base):
    __tablename__ = "cart_products"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    size_id = Column(Integer, ForeignKey('sizes.id'))
    quantity = Column(Integer, default=1)

    cart = relationship('Cart', back_populates='cart_products')
    product = relationship('Product', back_populates='cart_products')
    size = relationship('Size', back_populates='cart_products')


class Size(base):
    __tablename__ = "sizes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mult = Column(Float, default=1)

    cart_products = relationship('CartProduct', back_populates='size')


class BonusCard(base):
    __tablename__ = "bonus_card"
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    userId = relationship('User', back_populates='bonus_card')


class Role(base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    users_list = relationship('User', back_populates='roles', uselist=True)

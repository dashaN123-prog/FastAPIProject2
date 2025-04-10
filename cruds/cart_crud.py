from fastapi import Body, Depends
from sqlalchemy.orm import Session
from models.category_model import Category, Product, User, Cart, CartProduct, BonusCard, Role
from schemas.user_schema import UserBase, Roles


def get_all_products(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    # # cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    # # cart_products = (db.query(CartProduct).filter(CartProduct.cart_id == cart.id).all())
    # data = db.query(Product.name).join(CartProduct, Product.id == CartProduct.product_id).join(Cart,
    #                                                                                            CartProduct.cart_id == Cart.id).all()
    # print(data)
    return user

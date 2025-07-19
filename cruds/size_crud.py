from sqlalchemy.orm import Session
from models.category_model import Category, Product, User, Cart, CartProduct, BonusCard, Role, Size


def get_all_sizes(db: Session):
    sizes=db.query(Size).all()
    return sizes

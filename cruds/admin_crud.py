from fastapi import Body
from sqlalchemy.orm import Session
from models.category_model import Category, Product, User, Cart, CartProduct, BonusCard, Role
from schemas.user_schema import UserBase, Roles


def set_user_role(db: Session, phone_number, new_role_id):
    existing_user = db.query(User).filter_by(phone_number=phone_number).first()
    if existing_user is not None:
        existing_user.id_role = new_role_id
        db.commit()
        db.refresh(existing_user)
        return True
    else:
        return False


def create_role(db: Session, name):
    role = Role(name=name)
    db.add(role)
    db.commit()
    return True


def delete_role(db: Session, name):
    role = db.query(Role).filter_by(name=name).first()
    db.delete(role)
    db.commit()
    return True


def get_all_roles(db: Session):
    return db.query(Role).all()

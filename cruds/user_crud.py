from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from models.category_model import User, Cart, BonusCard
from schemas.user_schema import UserBase


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name.capitalize()).all()


def get_user_by_name_one(db: Session, name: str):
    return db.query(User).filter(User.name == name.capitalize()).first()


def add_user(db: Session, data: UserBase):
    new_user = User(name=data.name.capitalize(), age=data.age, tg_id=data.tg_id, phone_number=data.phone_number)
    new_user.cart = Cart()
    new_user.bonus_card = BonusCard()
    new_user.id_role = 1
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


def update_user(db: Session, name: str, data: UserBase):
    user = get_user_by_name_one(db, name)
    if user is None:
        return None
    else:
        user.name = data.name.capitalize()
        user.age = data.age
        user.phone_number = data.phone_number
        db.commit()
        db.refresh(user)
        return user


def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return False
    else:
        db.delete(user)
        db.commit()
        return True

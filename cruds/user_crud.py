from sqlalchemy.orm import Session
from models.user_model import User, Role


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return False
    return user


def get_user_by_tg_id(db: Session, tg_id: str):
    return db.query(User).filter(User.tg_id == tg_id).first()


def create_user(db: Session, user_data: dict):
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True


def update_user_role(db: Session, user_id: int, new_role_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == new_role_id).first()

    if user is None:
        return False
    if role is None:
        return None

    user.id_role = new_role_id
    db.commit()
    db.refresh(user)
    return user
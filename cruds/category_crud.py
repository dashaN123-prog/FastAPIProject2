from sqlalchemy.orm import Session
from models.category_model import Category


def get_category(db: Session):
    return db.query(Category).all()


def get_category_by_name(db: Session, name: str):
    category = db.query(Category).filter_by(name=name).first()
    if category is None:
        return False
    return category


def create_category(db: Session, category_name: str):
    new_category = Category(name=category_name)
    db.add(new_category)
    db.commit()


def delete_category(db: Session, category_name: str):
    category = db.query(Category).filter(Category.name == category_name).first()
    if category is None:
        return False
    else:
        db.delete(category)
        db.commit()
        return True


def update_category(db: Session, category_name: str, category_new_name):
    category = db.query(Category).filter(Category.name == category_name).first()
    if category is None:
        return False
    else:
        category.name = category_new_name
        db.commit()
        db.refresh(category)
        return True

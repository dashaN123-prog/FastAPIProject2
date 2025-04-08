from fastapi import Body
from sqlalchemy.orm import Session
from models.category_model import Category, Product
from schemas.product_schema import ProductBase


def get_products(db: Session):
    return db.query(Product).all()


def get_one_category_products(db: Session, category_name: str):
    cat = db.query(Category).filter_by(name=category_name).first()
    db.commit()
    if cat is None:
        return False
    else:
        return cat.products_list


# def create_product(db: Session, product_name: str, price: int, stock: int, description: str, img_url: str,
#                    age_restriction: int, category_id: int):
#     new_product = Product(name=product_name, price=price, stock=stock, description=description, img_url=img_url,
#                           age_restriction=age_restriction, category_id=category_id)
#     db.add(new_product)
#     db.commit()


def delete_product(db: Session, category_name: str, product_name: str):
    category = db.query(Category).filter_by(name=category_name).first()
    if category is None:
        return False

    product = db.query(Product).filter(Product.name == product_name,Product.category_id == category.id).first()

    if product is None:
        return None

    db.delete(product)
    db.commit()
    return True



def add_product(db: Session, data: ProductBase):
    new_product = Product(name=data.name, price=data.price, stock=data.stock,
                          description=data.description, img_url=data.img_url,
                          age_restriction=data.age_restriction, category_id=data.category_id)
    db.add(new_product)
    db.commit()
    db.close()


def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()


def update_product(db: Session, name: str, data: ProductBase):
    product = get_product_by_name(db, name)
    if product is None:
        return None
    else:
        product.price = data.price
        product.stock = data.stock
        db.commit()
        db.refresh(product)
        return product

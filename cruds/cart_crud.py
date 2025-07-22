from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.category_model import Product, User, Cart, CartProduct, Size

def add_product_to_cart(user_id:int, product_id:int, quantity:int, size_name:str, db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    size = db.query(Size).filter(Size.name == size_name).first()

    if not size:
        raise HTTPException(status_code=404, detail="Size not found")

    cart_prod = CartProduct(product_id=product_id, cart_id=cart.id, quantity=quantity, size_id=size.id)
    db.add(cart_prod)
    db.commit()
    db.refresh(cart_prod)

def del_all_prod_from_cart(user_id:int, db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    db.query(CartProduct).filter(CartProduct.cart_id == cart.id).delete()
    db.commit()



def get_all_products(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    result = (
        db.query(Product, Size, CartProduct)
        .join(Product, CartProduct.product_id == Product.id)
        .join(Size, Size.id == CartProduct.size_id)
        .filter(CartProduct.cart_id == cart.id)
        .all()
    )
    listprod = []
    for product, size, cartprod in result:
        listprod.append({
            "product_id": product.id,          # добавляем product_id
            "product_name": product.name,
            "product_price": product.price,
            "quantity": cartprod.quantity,
            "size": size.name,
            "size_mult": size.mult,
            "size_id": size.id                 # добавляем size_id
        })
    return listprod

def add_product_to_cart(user_id:int, product_id:int, quantity:int, size_name:str, db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    size = db.query(Size).filter(Size.name == size_name).first()

    if not size:
        raise HTTPException(status_code=404, detail="Size not found")

    cart_prod = CartProduct(product_id=product_id, cart_id=cart.id, quantity=quantity, size_id=size.id)
    db.add(cart_prod)
    db.commit()
    db.refresh(cart_prod)

def del_all_prod_from_cart(user_id:int, db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    db.query(CartProduct).filter(CartProduct.cart_id == cart.id).delete()
    db.commit()

def del_product_from_cart(user_id: int, product_id: int, size_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_product = db.query(CartProduct).filter(
        CartProduct.cart_id == cart.id,
        CartProduct.product_id == product_id,
        CartProduct.size_id == size_id
    ).first()

    if not cart_product:
        raise HTTPException(status_code=404, detail="Product not found in cart")

    db.delete(cart_product)
    db.commit()


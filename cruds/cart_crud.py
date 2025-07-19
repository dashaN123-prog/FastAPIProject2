from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from fastapi import HTTPException

from models.category_model import Product, User, Cart, CartProduct, Size


def get_all_products(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    result=(db.query(Product,Size,CartProduct).join(Product,CartProduct.product_id==Product.id).join(Size,Size.id==CartProduct.size_id).filter(CartProduct.cart_id==cart.id).all())
    listprod=[]
    for product,size,cartprod in result:
        listprod.append({"product_name":product.name,
                         "product_id": product.id,
                         "product_price":product.price,
                         "quantity":cartprod.quantity,
                         "size":size.name,
                         "size_mult":size.mult})
    return listprod

def add_product_to_cart(user_id:int, product_id:int, quantity:int, size_name:str,db:Session):
    user=db.query(User).filter(User.id==user_id).first()
    cart=db.query(Cart).filter(Cart.user_id==user.id).first()
    size=db.query(Size).filter(Size.name==size_name).first()
    cart_prod=CartProduct(product_id=product_id,cart_id=cart.id,quantity=quantity, size_id=size.id)
    db.add(cart_prod)
    db.commit()
    db.refresh(cart_prod)


def del_all_prod_from_cart(user_id:int,db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    products=db.query(CartProduct).filter(CartProduct.cart_id==cart.id).delete()
    db.commit()


def del_product_from_cart(user_id: int, product_id: int, db: Session):
    print(f"[DEBUG] Удаление товара: user_id={user_id}, product_id={product_id}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print("[DEBUG] Пользователь не найден")
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        print("[DEBUG] Корзина не найдена")
        raise HTTPException(status_code=404, detail="Cart not found")

    product_to_delete = db.query(CartProduct).filter(
        CartProduct.cart_id == cart.id,
        CartProduct.product_id == product_id
    ).first()

    if not product_to_delete:
        print("[DEBUG] Продукт не найден в корзине")
        raise HTTPException(status_code=404, detail="Product not found in cart")

    print("[DEBUG] Продукт найден, удаляю...")
    db.delete(product_to_delete)
    db.commit()
    print("[DEBUG] Удаление завершено")



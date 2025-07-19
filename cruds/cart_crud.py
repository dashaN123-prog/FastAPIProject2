from http.client import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from models.category_model import Product, User, Cart, CartProduct, Size


def get_all_products(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    result=(db.query(Product,Size,CartProduct).join(Product,CartProduct.product_id==Product.id).join(Size,Size.id==CartProduct.size_id).filter(CartProduct.cart_id==cart.id).all())
    listprod=[]
    for product,size,cartprod in result:
        listprod.append({"product_name":product.name,
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
    db.close()

def del_all_prod_from_cart(user_id:int,db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    products=db.query(CartProduct).filter(CartProduct.cart_id==cart.id).delete()
    db.commit()
    db.close()

def del_product_from_cart(user_id: int, product_id: int, size_name: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    size = db.query(Size).filter(Size.name == size_name).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")

    cart_product = db.query(CartProduct).filter(
        CartProduct.cart_id == cart.id,
        CartProduct.product_id == product_id,
        CartProduct.size_id == size.id
    ).first()

    if not cart_product:
        raise HTTPException(status_code=404, detail="Product not found in cart")

    db.delete(cart_product)
    db.commit()

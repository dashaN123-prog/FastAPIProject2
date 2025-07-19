from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.category_model import Product, User, Cart, CartProduct, Size

def get_all_products(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        return []

    results = (db.query(Product, Size, CartProduct)
               .join(CartProduct, CartProduct.product_id == Product.id)
               .join(Size, Size.id == CartProduct.size_id)
               .filter(CartProduct.cart_id == cart.id)
               .all())

    products_list = []
    for product, size, cartprod in results:
        products_list.append({
            "product_name": product.name,
            "product_id": product.id,
            "product_price": product.price,
            "quantity": cartprod.quantity,
            "size": size.name,
            "size_mult": size.mult
        })

    return products_list


def add_product_to_cart(user_id: int, product_id: int, quantity: int, size_name: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        # Создаем корзину, если нет
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    size = db.query(Size).filter(Size.name == size_name).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")

    # Проверяем, есть ли уже такой товар с этим размером в корзине
    cart_product = (db.query(CartProduct)
                    .filter(CartProduct.cart_id == cart.id,
                            CartProduct.product_id == product_id,
                            CartProduct.size_id == size.id)
                    .first())

    if cart_product:
        cart_product.quantity += quantity
    else:
        cart_product = CartProduct(
            product_id=product_id,
            cart_id=cart.id,
            quantity=quantity,
            size_id=size.id
        )
        db.add(cart_product)

    db.commit()
    db.refresh(cart_product)
    return cart_product


def del_all_prod_from_cart(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        return

    db.query(CartProduct).filter(CartProduct.cart_id == cart.id).delete()
    db.commit()


def del_product_from_cart(user_id: int, product_id: int, db: Session) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        return False

    cart_product = db.query(CartProduct).filter(
        CartProduct.cart_id == cart.id,
        CartProduct.product_id == product_id
    ).first()

    if not cart_product:
        return False

    db.delete(cart_product)
    db.commit()
    return True

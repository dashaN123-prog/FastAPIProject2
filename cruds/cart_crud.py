from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.category_model import Product, User, Cart, CartProduct, Size

def get_all_products(user_id: int, db: Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return []

    products = (
        db.query(
            Product.name.label("product_name"),
            Product.price.label("product_price"),
            Size.name.label("size"),
            Size.multiplier.label("size_mult"),
            CartProduct.quantity,
            Product.id.label("product_id")
        )
        .join(CartProduct, CartProduct.product_id == Product.id)
        .join(Size, Size.id == CartProduct.size_id)
        .filter(CartProduct.cart_id == cart.id)
        .all()
    )

    return products


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


def del_product_from_cart(user_id: int, product_id: int, size_name: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(404, "Cart not found")

    size = db.query(Size).filter(Size.name == size_name).first()
    if not size:
        raise HTTPException(404, "Size not found")

    cart_prod = db.query(CartProduct).filter(
        CartProduct.cart_id == cart.id,
        CartProduct.product_id == product_id,
        CartProduct.size_id == size.id
    ).first()
    if not cart_prod:
        raise HTTPException(404, "Product not in cart")

    db.delete(cart_prod)
    db.commit()


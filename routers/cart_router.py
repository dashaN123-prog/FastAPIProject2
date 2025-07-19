from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from cruds.cart_crud import get_all_products, add_product_to_cart, del_all_prod_from_cart, del_product_from_cart
from database import get_db

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("/{user_id}")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return get_all_products(user_id, db)

@router.post("/")
def create_cart_prods(user_id: int = Body(embed=True),prod_id:int=Body(embed=True),quant:int=Body(embed=True),size:str=Body(embed=True), db: Session = Depends(get_db)):
    add_product_to_cart(user_id,prod_id,quant,size,db)
    return JSONResponse(content={"message": "prod added to cart succ"}, status_code=status.HTTP_201_CREATED)

@router.delete("/{user_id}")
def del_cart_prods(user_id: int, db: Session = Depends(get_db)):
    del_all_prod_from_cart(user_id, db)
    return JSONResponse(content={"message": "del succ"}, status_code=status.HTTP_200_OK)

@router.delete("/{user_id}/product/{product_id}")
def delete_product_from_cart(
    user_id: int,
    product_id: int,
    size: str,  # теперь size из query параметров
    db: Session = Depends(get_db)
):
    del_product_from_cart(user_id, product_id, size, db)
    return JSONResponse({"message": "Product removed from cart"}, status_code=status.HTTP_200_OK)

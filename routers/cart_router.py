from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from cruds.cart_crud import get_all_products, add_product_to_cart, del_all_prod_from_cart, del_product_from_cart
from database import get_db
from models.category_model import User, Cart, CartProduct

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
def delete_product_from_cart_endpoint(user_id: int, product_id: int, db: Session = Depends(get_db)):
    try:
        print(f"Request to delete product_id={product_id} from user_id={user_id}'s cart")
        del_product_from_cart(user_id, product_id, db)
        print("Deletion successful")
        return JSONResponse(content={"message": "Product deleted"}, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)





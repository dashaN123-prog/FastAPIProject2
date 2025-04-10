from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from cruds.cart_crud import get_all_products
from cruds.category_crud import get_category, create_category, delete_category, update_category
from database import get_db

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("/")
async def get_cart(user_id: int = Body(embed=True), db: Session = Depends(get_db)):
    return get_all_products(user_id, db)

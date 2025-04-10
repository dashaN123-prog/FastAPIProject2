from typing import Optional

from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi import FastAPI, Body
from starlette import status
from starlette.responses import JSONResponse

from database import get_db
from cruds.product_crud import get_products, get_one_category_products, add_product, delete_product, update_product, \
    get_product_by_name
from sqlalchemy.orm import Session

from schemas.product_schema import ProductBase

router = APIRouter(prefix='/api/products', tags=["products"])


@router.get("/")
def root(name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if name:
        return get_product_by_name(db, name)
    return get_products(db)


@router.get('/{category_name}')
def get_products_by_category_name(category_name: str, db: Session = Depends(get_db)):
    return get_one_category_products(db, category_name)


@router.post('/')
def create_new_product(data: ProductBase, db: Session = Depends(get_db)):
    add_product(db, data)
    return JSONResponse(content={"message": "Prod created succ"}, status_code=status.HTTP_201_CREATED)


# @router.post("/")
# async def create_products(name: str = Body(embed=True), price: int = Body(embed=True), stock: int = Body(embed=True),
#                           description: str = Body(embed=True), img_url: str = Body(embed=True),
#                           age_restriction: int = Body(embed=True), category_id: int = Body(embed=True),
#                           db: Session = Depends(get_db)):
#     create_product(db, name, price, stock, description, img_url, age_restriction, category_id)
#     return JSONResponse(content={"message": "Prod created succ"}, status_code=status.HTTP_201_CREATED)


@router.delete("/{name}")
async def del_products(name, db: Session = Depends(get_db)):
    if delete_product(db, name):
        return JSONResponse(content={"message": "Prod deleted succ"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Prod not found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{name}")
def update_products(name: str, data: ProductBase, db: Session = Depends(get_db)):
    product = update_product(db, name, data)
    if product is None:
        return JSONResponse(content={"message": "Prod not found"}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        j = jsonable_encoder(product)
        return JSONResponse(content=j, status_code=status.HTTP_200_OK)

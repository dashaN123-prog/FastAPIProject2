from typing import Optional

from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi import FastAPI, Body
from starlette import status
from starlette.responses import JSONResponse

from cruds.admin_crud import set_user_role
from cruds.product_crud import get_product_by_name
from cruds.user_crud import get_users, get_user_by_name, add_user, update_user, delete_user
from database import get_db
from sqlalchemy.orm import Session

from schemas.product_schema import ProductBase
from schemas.user_schema import UserBase

router = APIRouter(prefix='/api/users', tags=["users"])


@router.get("/")
def user_get(name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if name:
        return get_user_by_name(db, name)
    return get_users(db)


@router.post('/')
def create_new_user(data: UserBase, db: Session = Depends(get_db)):
    add_user(db, data)
    return JSONResponse(content={"message": "User created succ"}, status_code=status.HTTP_201_CREATED)


@router.patch("/{name}")
def update_products(name: str, data: UserBase, db: Session = Depends(get_db)):
    user = update_user(db, name, data)
    if user is None:
        return JSONResponse(content={"message": "Prod not found"}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        j = jsonable_encoder(user)
        return JSONResponse(content=j, status_code=status.HTTP_200_OK)


@router.delete("/{id}")
async def del_user(id, db: Session = Depends(get_db)):
    if delete_user(db, id):
        return JSONResponse(content={"message": "Prod deleted succ"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Prod not found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/admin/{phone_number}")
def change_role(phone_number: str, new_role_id: int = Body(embed=True), db: Session = Depends(get_db)):
    if set_user_role(db, phone_number, new_role_id):
        return JSONResponse(content={"message": "Role updated"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "No user found"}, status_code=status.HTTP_404_NOT_FOUND)

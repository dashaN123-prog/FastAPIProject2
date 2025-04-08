from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from database import get_db
from cruds.user_crud import (get_users, get_user_by_id, get_user_by_tg_id,
                             create_user, delete_user, update_user_role)
from schemas.user_schema import UserBase, UserResponse, UserRoleUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is False:
        return JSONResponse(content={"message": "User not found"},status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.post("/")
async def create_new_user(data: UserBase, db: Session = Depends(get_db)):
    try:
        user = create_user(db, data.dict())
        return JSONResponse(content={"message": "User created successfully", "id": user.id},status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    if delete_user(db, user_id):
        return JSONResponse(content={"message": "User deleted successfully"},status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "User not found"},status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{user_id}/role")
async def update_user_role_endpoint(
        user_id: int,
        data: UserRoleUpdate,
        db: Session = Depends(get_db)):
    result = update_user_role(db, user_id, data.id_role)

    if result is False:
        return JSONResponse(content={"message": "User not found"},status_code=status.HTTP_404_NOT_FOUND)
    if result is None:
        return JSONResponse(content={"message": "Role not found"},status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content={"message": "Role updated successfully"},status_code=status.HTTP_200_OK)
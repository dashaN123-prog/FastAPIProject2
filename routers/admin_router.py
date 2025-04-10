from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from cruds.admin_crud import set_user_role, create_role, delete_role, get_all_roles
from cruds.category_crud import get_category, create_category, delete_category, update_category
from database import get_db

router = APIRouter(prefix='/api/admin', tags=["admin"])


@router.patch("/roles/update")
def change_role(phone_number: str = Body(embed=True), new_role_id: int = Body(embed=True),
                db: Session = Depends(get_db)):
    if set_user_role(db, phone_number, new_role_id):
        return JSONResponse(content={"message": "Role updated"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "No user found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.post("/roles")
def create_roles(name: str = Body(embed=True), db: Session = Depends(get_db)):
    if create_role(db, name):
        return JSONResponse(content={"message": "Role created"}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"message": "Not created"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/roles")
def delete_roles(name: str = Body(embed=True), db: Session = Depends(get_db)):
    if delete_role(db, name):
        return JSONResponse(content={"message": "Role deleted"}, status_code=status.HTTP_202_ACCEPTED)
    else:
        return JSONResponse(content={"message": "Not deleted"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    roles = get_all_roles(db)
    if roles is None:
        return JSONResponse(content={"message": "No user found"}, status_code=status.HTTP_404_NOT_FOUND)
    return roles


@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    return get_category(db)


@router.post("/categories")
async def create_categories(name: str = Body(embed=True), db: Session = Depends(get_db)):
    create_category(db, name)
    return JSONResponse(content={"message": "Category created successfully"}, status_code=status.HTTP_201_CREATED)


@router.delete("/categories/{name}")
async def delete_categories(name, db: Session = Depends(get_db)):
    if delete_category(db, name):
        return JSONResponse(content={"message": "Category deleted successfully"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.put("/categories/{name}")
async def update_categories(name, new_name: str = Body(embed=True), db: Session = Depends(get_db)):
    if update_category(db, name, new_name):
        return JSONResponse(content={"message": "Category updated successfully"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=status.HTTP_404_NOT_FOUND)

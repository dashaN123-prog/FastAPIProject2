from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from cruds.category_crud import get_category, create_category, delete_category, update_category
from database import get_db

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    return get_category(db)


@router.post("/")
async def create_categories(name: str = Body(embed=True), db: Session = Depends(get_db)):
    create_category(db, name)
    return JSONResponse(content={"message": "Category created successfully"}, status_code=status.HTTP_201_CREATED)


@router.delete("/{name}")
async def delete_categories(name, db: Session = Depends(get_db)):
    if delete_category(db, name):
        return JSONResponse(content={"message": "Category deleted successfully"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{name}")
async def update_categories(name, new_name: str = Body(embed=True), db: Session = Depends(get_db)):
    if update_category(db, name, new_name):
        return JSONResponse(content={"message": "Category updated successfully"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=status.HTTP_404_NOT_FOUND)

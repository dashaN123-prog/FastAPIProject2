from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from cruds.size_crud import get_all_sizes
from database import get_db

router = APIRouter(prefix="/api/size", tags=["size"])


@router.get("/")
def get_size(db: Session = Depends(get_db)):
    return get_all_sizes(db)
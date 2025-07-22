from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(max_length=50)
    age: int = Field(gt=12, le=100)
    tg_id: str = Field()
    phone_number: str = Field(20)


class CartBase(BaseModel):
    user_id: int = Field()


class SizeBase(BaseModel):
    name: str
    mult: float


class CartProductBase(BaseModel):
    product_id: int
    quantity: int = Field(default=1)
    size_id: int


class BonusCardBase(BaseModel):
    balance: int = Field(default=0)
    user_id: int = Field()


class Roles(BaseModel):
    name: str = Field(max_length=50)



class CartProductResponse(BaseModel):
    product_id: int
    product_name: str
    product_price: int
    quantity: int
    size: str
    size_mult: float
    size_id: int

    class Config:
        orm_mode = True

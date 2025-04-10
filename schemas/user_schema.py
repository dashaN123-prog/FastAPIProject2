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

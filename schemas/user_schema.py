from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(max_length=50)
    age: int | None = Field(default=None)
    tg_id: str = Field(max_length=255)
    phone_number: str = Field(max_length=20)
    id_role: int = Field(default=1)


class UserResponse(UserBase):
    id: int


class UserRoleUpdate(BaseModel):
    id_role: int = Field(ge=1, description="ID of the new role (1-user, 2-manager, 3-admin)")
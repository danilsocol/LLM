from pydantic import BaseModel

from models.Enum.user_role import UserRole


class UserResponse(BaseModel):
    id: int
    email: str
    password: str
    role: UserRole
    organization_id: int
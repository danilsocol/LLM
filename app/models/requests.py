from pydantic import BaseModel

from models.organization import Organization


class LoginRequest(BaseModel):
    email: str
    password: str

class CreateOrgRequest(BaseModel):
    organization: Organization
    user_id: int

class CreateDocumentRequest(BaseModel):
    title: str
    content: str
    organization_id: int
    modified_by_id: int

class CoinRequest(BaseModel):
    user_id: int
    coins: int

class AddUserRequest(BaseModel):
    admin_id: int

class UserIdRequest(BaseModel):
    user_id: int
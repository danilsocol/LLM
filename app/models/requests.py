from pydantic import BaseModel

from models.organization import Organization


class LoginRequest(BaseModel):
    email: str
    password: str

class CreateOrgRequest(BaseModel):
    organization: Organization
    user_id: int
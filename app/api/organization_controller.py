from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.database import get_session
from models.Enum.user_role import UserRole
from models.organization import Organization
from models.requests import (CreateOrgRequest,CoinRequest)
from services.organization import (
    create_organization,
    get_organization_by_id,
    update_organization_admin,
    update_organization_name,
    add_coins_to_organization,
    add_user_to_organization,
    remove_user_from_organization,
    remove_organization
)
from services.user import (change_user_role,get_users_by_organization,get_user_by_id)

from app.models.user import User

router = APIRouter()

@router.post("/organizations/", response_model=Organization)
async def create_new_organization(organization_req: CreateOrgRequest, session: Session = Depends(get_session)):
    org = create_organization(organization_req.organization, session)
    updated_user = change_user_role(organization_req.user_id, UserRole.ORG_ADMIN, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User  not found")

    add_user_to_organization(organization_req.user_id, org.id, session)

    session.commit()
    session.refresh(org)
    return org

@router.get("/organizations/{organization_id}", response_model=Organization)
async def get_organization(organization_id: int, session: Session = Depends(get_session)):
    organization = get_organization_by_id(organization_id, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.put("/organizations/{organization_id}/admin", response_model=Organization)
async def update_admin(organization_id: int, new_admin_id: int, session: Session = Depends(get_session)):
    organization = update_organization_admin(organization_id, new_admin_id, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.put("/organizations/{organization_id}/name", response_model=Organization)
async def update_name(organization_id: int, new_name: str, session: Session = Depends(get_session)):
    organization = update_organization_name(organization_id, new_name, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.post("/organizations/{organization_id}/coins", response_model=Organization)
async def add_coins(organization_id: int, coin_request: CoinRequest, session: Session = Depends(get_session)):
    organization = add_coins_to_organization(organization_id,coin_request.coins, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.post("/organizations/{organization_id}/users/{user_id}", response_model=User)
async def add_user(organization_id: int, admin_id : int , user_id: int, session: Session = Depends(get_session)):
    admin = get_user_by_id(admin_id, session)
    if(admin and
            (admin.role == UserRole.ORG_ADMIN
             or admin.role == UserRole.ADMIN) and admin.organization_id == organization_id):
        user = add_user_to_organization(organization_id, user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    else:
        raise HTTPException(status_code=403, detail="You are not an admin")


@router.delete("/organizations/{organization_id}/users/{user_id}", response_model=Organization)
async def remove_user(organization_id: int, user_id: int, session: Session = Depends(get_session)):
    organization = remove_user_from_organization(organization_id, user_id, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization or user not found")
    return organization

@router.post("/organizations/{organization_id}/leave")
async def leave_organization(organization_id: int, user_id: int, session: Session = Depends(get_session)):
    removed = remove_user_from_organization(user_id, organization_id, session)
    if not removed:
        raise HTTPException(status_code=404, detail="User  not found in organization")

    session.commit()
    return {"detail": "User  successfully left the organization"}


@router.delete("/organizations/{organization_id}")
async def leave_organization(organization_id: int, session: Session = Depends(get_session)):
    users = get_users_by_organization(organization_id, session)

    for user in users:
        change_user_role(user.id, UserRole.NONE, session)

    remove_organization(organization_id, session)

    session.commit()
    return {"detail": "Organization and all associated users successfully removed"}
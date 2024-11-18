from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.database import get_session
from models.organization import Organization
from services.organization import (
    create_organization,
    get_organization_by_id,
    update_organization_admin,
    update_organization_name,
    add_coins_to_organization,
    add_user_to_organization,
    remove_user_from_organization,
)

router = APIRouter()

@router.post("/organizations/", response_model=Organization)
async def create_new_organization(organization: Organization, session: Session = Depends(get_session)):
    create_organization(organization, session)
    return organization

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

@router.put("/organizations/{organization_id}/coins", response_model=Organization)
async def add_coins(organization_id: int, coins_to_add: int, session: Session = Depends(get_session)):
    organization = add_coins_to_organization(organization_id, coins_to_add, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.post("/organizations/{organization_id}/users/{user_id}", response_model=Organization)
async def add_user(organization_id: int, user_id: int, session: Session = Depends(get_session)):
    organization = add_user_to_organization(organization_id, user_id, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization or user not found")
    return organization

@router.delete("/organizations/{organization_id}/users/{user_id}", response_model=Organization)
async def remove_user(organization_id: int, user_id: int, session: Session = Depends(get_session)):
    organization = remove_user_from_organization(organization_id, user_id, session)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization or user not found")
    return organization

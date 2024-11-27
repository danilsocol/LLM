from models.organization import Organization
from models.user import User
from typing import List, Optional

from models.Enum.user_role import UserRole


def create_organization(new_admin_id: int, new_organization: Organization, session) -> Optional[Organization]:
    org = Organization(name = new_organization.name)
    session.add(org)

    user = session.get(User, new_admin_id)
    user.organization_id = org.id
    user.role = UserRole.ORG_ADMIN

    return org

def get_organization_by_id(id: int, session) -> Optional[Organization]:
    organization = session.query(Organization).filter(Organization.id == id).first()
    if organization:
        return organization
    return None

def update_organization_admin(organization_id: int, new_admin_id: int, session) -> None:
    organization = get_organization_by_id(organization_id, session)
    if organization:
        organization.admin_id = new_admin_id
        session.commit()

def add_coins_to_organization(organization_id: int, coins_amount: int, session) -> Organization:
    organization = get_organization_by_id(organization_id, session)
    if organization:
        organization.coins += coins_amount
        return organization

def update_organization_name(organization_id: int, new_name: str, session) -> None:
    organization = get_organization_by_id(organization_id, session)
    if organization:
        organization.name = new_name
        session.commit()

def add_user_to_organization(user_id: int, organization_id: int, session) -> None:
    user = session.get(User, user_id)
    if user and user.organization_id is None:
        user.organization_id = organization_id
        user.role = UserRole.USER
        session.commit()
        session.refresh(user)
        return user

def remove_user_from_organization(user_id: int, session) -> None:
    user = session.get(User, user_id)
    if user:
        user.organization_id = None
        user.role = UserRole.NONE

def remove_organization(organization_id: int, session) -> None:
    organization = get_organization_by_id(organization_id, session)
    session.delete(organization)


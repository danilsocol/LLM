from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from auth.jwt_handler import TokenData, verify_access_token
from database.database import get_session
from models.document import Document
from services.document import (
    get_document_by_id,
    create_document,
    update_document,
    get_all_documents,
    get_documents_by_organization,
)

from models.requests import CreateDocumentRequest

from services.document import delete_document_from_db

router = APIRouter()

@router.get("/documents/{document_id}", response_model=Document)
async def get_document(document_id: int,token_data: TokenData = Depends(verify_access_token), session: Session = Depends(get_session)):
    document = get_document_by_id(document_id, session)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.post("/organizations/{organization_id}/documents", response_model=Document)
async def create_new_document(documentRequest: CreateDocumentRequest, token_data: TokenData = Depends(verify_access_token), session: Session = Depends(get_session)):
    document = Document(title=documentRequest.title, content=documentRequest.content,
                        organization_id=documentRequest.organization_id,
                        modified_by_id=documentRequest.modified_by_id)

    create_document(document, session)
    return document

@router.put("/documents/{document_id}", response_model=Document)
async def update_existing_document(document_id: int, documentRequest: CreateDocumentRequest,token_data: TokenData = Depends(verify_access_token), session: Session = Depends(get_session)):
    document = update_document(document_id, documentRequest, session)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.get("/documents/", response_model=List[Document])
async def get_all_documents_route(token_data: TokenData = Depends(verify_access_token),session: Session = Depends(get_session)):
    documents = get_all_documents(session)
    return documents

@router.get("/organizations/{organization_id}/documents", response_model=List[Document])
async def get_organization_documents(organization_id: int,token_data: TokenData = Depends(verify_access_token), session: Session = Depends(get_session)):
    documents = get_documents_by_organization(organization_id, session)
    return documents

@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(document_id: int,token_data: TokenData = Depends(verify_access_token), session: Session = Depends(get_session)):
    document = get_document_by_id(document_id, session)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    delete_document_from_db(document, session)
    return
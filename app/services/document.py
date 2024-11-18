from models.document import Document
from typing import List, Optional

def get_document_by_id(id: int, session) -> Optional[Document]:
    document = session.get(Document, id)
    if document:
        return document
    return None

def create_document(new_document: Document, session) -> None:
    session.add(new_document)
    session.commit()
    session.refresh(new_document)

def update_document(document_id: int, updated_document: Document, session) -> Optional[Document]:
    document = session.get(Document, document_id)
    if document:
        for key, value in updated_document.dict().items():
            setattr(document, key, value)
        session.commit()
        session.refresh(document)
        return document
    return None

def get_all_documents(session) -> List[Document]:
    return session.query(Document).all()

def get_documents_by_organization(organization_id: int, session) -> List[Document]:
    return session.query(Document).filter(Document.organization_id == organization_id).all()
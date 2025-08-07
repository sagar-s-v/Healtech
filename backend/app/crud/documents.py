from sqlalchemy.orm import Session
from app.db import models
from app.schemas import document as schemas

# This is our test message. If we see this, the file is being loaded correctly.
print("--- CRUD/DOCUMENTS.PY FILE HAS BEEN LOADED ---")

def get_document(db: Session, doc_id: int):
    """Fetches a single document by its ID."""
    return db.query(models.Document).filter(models.Document.id == doc_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    """Fetches a list of all documents."""
    return db.query(models.Document).offset(skip).limit(limit).all()

def create_document(db: Session, doc: schemas.DocumentCreate):
    """Creates a new document record in the database."""
    db_doc = models.Document(file_name=doc.file_name, document_type=doc.document_type)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def update_document_status(db: Session, doc_id: int, status: str):
    """Updates the status of an existing document."""
    db_doc = get_document(db, doc_id)
    if db_doc:
        db_doc.status = status
        db.commit()
        db.refresh(db_doc)
    return db_doc
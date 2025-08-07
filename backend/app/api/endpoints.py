#highlight-start
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
# highlight-end
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import documents as doc_crud
from app.schemas import document as doc_schemas
from app.services import document_processor, vector_store, llm_handler

router = APIRouter()

@router.post("/upload/", response_model=doc_schemas.Document)
async def upload_document(
    file: UploadFile = File(...),
    doc_type: str = Form(...),
    db: Session = Depends(get_db)
):
    # ... (no changes in this function)
    # 1. Create DB record
    db_doc = doc_crud.create_document(db, doc_schemas.DocumentCreate(file_name=file.filename, document_type=doc_type))

    # 2. Read and process file content
    contents = await file.read()
    try:
        if doc_type == "pdf":
            text = document_processor.extract_text_from_pdf(contents)
        elif doc_type == "docx":
            text = document_processor.extract_text_from_docx(contents)
        elif doc_type == "eml":
            text = document_processor.extract_text_from_eml(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported document type")
    except Exception as e:
        doc_crud.update_document_status(db, db_doc.id, "error_parsing")
        raise HTTPException(status_code=500, detail=f"Failed to parse document: {e}")

    # 3. Split text into chunks
    chunks = document_processor.split_text_into_chunks(text)

    # 4. Upsert chunks to vector store
    try:
        vector_store.upsert_chunks(doc_id=db_doc.id, chunks=chunks)
    except Exception as e:
        doc_crud.update_document_status(db, db_doc.id, "error_vectorizing")
        raise HTTPException(status_code=500, detail=f"Failed to vectorize document: {e}")

    # 5. Update status to 'ready'
    doc_crud.update_document_status(db, db_doc.id, "ready")

    return db_doc


# highlight-start
# MODIFIED FUNCTION
@router.post("/query/", response_model=doc_schemas.QueryResponse)
async def query_document(
    request_body: doc_schemas.QueryRequest,
    request: Request, # Inject the request object
    db: Session = Depends(get_db)
):
# highlight-end
    # 1. Check if document exists and is ready
# highlight-start
    db_doc = doc_crud.get_document(db, request_body.document_id)
# highlight-end
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if db_doc.status != "ready":
        raise HTTPException(status_code=400, detail=f"Document is not ready for querying. Status: {db_doc.status}")

    # 2. Retrieve relevant context from vector store
    try:
# highlight-start
        context = vector_store.query_vector_store(query=request_body.query, doc_id=request_body.document_id)
# highlight-end
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying vector store: {e}")

    if not context:
        return doc_schemas.QueryResponse(
            answer="Could not determine an answer.",
            conditions=[],
            rationale="No relevant information was found in the document for the given query.",
            retrieved_clauses=[]
        )

# highlight-start
    # Check for client disconnection before the expensive LLM call
    if await request.is_disconnected():
        print("Client disconnected, cancelling LLM call.")
        return # Or raise a specific exception

    # 3. Get response from LLM
    llm_response = llm_handler.get_llm_response(request_body.query, context)
# highlight-end

    return doc_schemas.QueryResponse(**llm_response)

@router.get("/documents/", response_model=list[doc_schemas.Document])
def list_documents(db: Session = Depends(get_db)):
    return doc_crud.get_documents(db)
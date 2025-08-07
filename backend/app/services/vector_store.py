# 1. Import ServerlessSpec alongside Pinecone
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from app.core.config import settings

# Initialize the Pinecone client object
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Initialize Sentence Transformer model
model = SentenceTransformer(settings.EMBEDDING_MODEL)
embedding_dim = model.get_sentence_embedding_dimension()

def get_or_create_index():
    index_name = settings.PINECONE_INDEX_NAME
    
    if index_name not in pc.list_indexes().names():
        # 2. Add the required 'spec' argument here
        pc.create_index(
            name=index_name,
            dimension=embedding_dim,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        
    # Connect to the index
    return pc.Index(index_name)

# Get a handle to the index
index = get_or_create_index()

def upsert_chunks(doc_id: int, chunks: list[str]):
    vectors_to_upsert = []
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        metadata = {'document_id': doc_id, 'text': chunk}
        vector_id = f"doc_{doc_id}_chunk_{i}"
        vectors_to_upsert.append((vector_id, embedding, metadata))

    # Upsert in batches
    batch_size = 100
    for i in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[i:i + batch_size]
        index.upsert(vectors=batch)

def query_vector_store(query: str, doc_id: int, top_k: int = 5) -> list[str]:
    query_embedding = model.encode(query).tolist()
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={"document_id": {"$eq": doc_id}}
    )
    
    contexts = [match['metadata']['text'] for match in results['matches']]
    return contexts
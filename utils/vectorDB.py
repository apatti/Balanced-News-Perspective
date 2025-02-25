import os
from agno.vectordb.pineconedb import PineconeDb

api_key = os.getenv("PINECONE_API_KEY")
index_name = "news-source"

vector_db = PineconeDb(
    name=index_name,
    dimension=1536,
    metric="cosine",
    api_key = api_key,
    use_hybrid_search=True
)
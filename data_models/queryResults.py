from pydantic import BaseModel, Field
from article import Article

class QueryResults(BaseModel):
    articles: list[Article] = Field(..., description="List of articles returned by the query.")
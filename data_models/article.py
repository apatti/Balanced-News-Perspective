from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="link to the article.")
    summary: str = Field(..., description="Summary of the article.")
    published_date: str = Field(..., description="Date when the article was published.")
from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="link to the article.")
    summary: str = Field(..., description="Summary of the article.")
    published_date: str = Field(..., description="Date when the article was published.")

class QueryResults(BaseModel):
    articles: list[Article] = Field(..., description="List of articles returned by the query.")

class ArticleContent(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="link to the article.")
    summary: str = Field(..., description="Summary of the article.")
    published_date: str = Field(..., description="Date when the article was published")
    content: str = Field(..., description="Full content of the article in markdown format. This field is optional and may not be present in all cases.")
    
class ViewPoint(BaseModel):
    title: str = Field(..., description="Title of the article.")
    urls: list[str] = Field(..., description="List of articles urls that provides the content to generate the view point.")
    summary: str = Field(..., description="Summary of the article from a specific perspective")
    content: list[str] = Field(..., description="Bullet points of the article content from a specific perspective.")
    prespective: str = Field(..., description="Bias, it would have one of the following values: left, right, center, neutral.")

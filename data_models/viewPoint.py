from pydantic import BaseModel, Field

class ViewPoint(BaseModel):
    title: str = Field(..., description="Title of the article.")
    urls: list[str] = Field(..., description="List of articles urls that provides the content to generate the view point.")
    summary: str = Field(..., description="Summary of the article from a specific perspective")
    content: list[str] = Field(..., description="Bullet points of the article content from a specific perspective.")
    prespective: str = Field(..., description="Bias, it would have one of the following values: left, right, center, neutral.")
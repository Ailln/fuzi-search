from pydantic import BaseModel


class Question(BaseModel):
    question: str
    threshold: float = 0.9
    limit: int = 5

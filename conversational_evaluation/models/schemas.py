from pydantic import BaseModel
from typing import Dict, List, Optional


class MessageItem(BaseModel):
    message: str
    metadata: Dict

class BeliefResult(BaseModel):
    belief: str
    interpretation: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    category: Optional[str] = None
    categories: Optional[List[str]] = None

class BeliefResponse(BaseModel):
    beliefs: List[BeliefResult]
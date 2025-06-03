from fastapi import APIRouter
from typing import List, Dict

from conversational_evaluation.models.schemas import MessageItem, BeliefResponse
from conversational_evaluation.services.evaluator import extract_beliefs

router = APIRouter()

@router.post("/evaluate", response_model=BeliefResponse)
def evaluate_conversation(conversation: List[MessageItem]):
    beliefs = extract_beliefs(conversation)
    return beliefs

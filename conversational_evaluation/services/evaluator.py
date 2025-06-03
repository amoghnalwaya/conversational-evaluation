import logging
from openai import OpenAI
from typing import List, Dict

from conversational_evaluation.models.schemas import MessageItem, BeliefResponse
from conversational_evaluation.utils.sentiment import SentimentAnalyzer
from conversational_evaluation.utils.belief_categorizer import assign_categories_to_beliefs

SYSTEM_PROMPT = (
    "You are an assistant that extracts belief statements and self-perceptions from a conversation. "
    "Given the conversation history, identify statements by the user that reveal their beliefs about themselves, "
    "especially any negative or distorted self-perceptions. Respond with a JSON array of beliefs, where each belief has "
    "a 'belief' and an 'interpretation'."
)

sentiment_analyzer = SentimentAnalyzer()

def build_prompt(conversation: List[MessageItem]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": build_conversation_text(conversation) +
                       "\n\nExtract the user's belief statements and return them in JSON format as: \n"
                       "{\"beliefs\": [ {\"belief\": ..., \"interpretation\": ... }, ... ]}"
        }
    ]
    return messages

def build_conversation_text(conversation: List[MessageItem]) -> str:
    lines = []
    for item in conversation:
        speaker = item.metadata.get("speaker", "unknown").capitalize()
        lines.append(f"{speaker}: {item.message}")
    return "\n".join(lines)

def extract_beliefs(conversation: List[MessageItem]) -> Dict:
    client = OpenAI()
    try:
        messages = build_prompt(conversation)
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=messages,
            response_format=BeliefResponse
        )
        parsed_response = response.choices[0].message.parsed
        beliefs = parsed_response.beliefs

        texts = [b.belief for b in beliefs]
        sentiments = sentiment_analyzer.score(texts)
        for b, s in zip(beliefs, sentiments):
            b.sentiment = s["label"]
            b.sentiment_score = s["score"]

        beliefs = assign_categories_to_beliefs(beliefs)

        return {"beliefs": [b.model_dump() for b in beliefs]}

    except Exception as e:
        logging.error(e)
        return {"beliefs": []}

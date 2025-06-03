import re
from typing import List
from conversational_evaluation.models.schemas import BeliefResult

COGNITIVE_DISTORTIONS = {
    "All-or-Nothing Thinking": [
        r"\b(always|never|completely|totally|entirely|no one|everyone)\b",
    ],
    "Overgeneralization": [
        r"\b(nothing ever works|everything goes wrong|I can never)\b",
    ],
    "Mental Filtering": [
        r"\b(ignore the positive|focus only on the negative)\b",
    ],
    "Disqualifying the Positive": [
        r"\b(doesn't count|wasn't really me|was just luck)\b",
    ],
    "Jumping to Conclusions": [
        r"\b(he must hate me|they think I'm stupid|they're ignoring me)\b",
    ],
    "Catastrophizing": [
        r"\b(ruined everything|this is the worst|I'm doomed)\b",
    ],
    "Labeling and Mislabeling": [
        r"\b(I am a failure|I'm stupid|I'm worthless)\b",
    ],
    "Personalization": [
        r"\b(it's my fault|I caused this|they're mad because of me)\b",
    ],
    "Should Statements": [
        r"\b(should have|must do|ought to|have to)\b",
    ],
    "Emotional Reasoning": [
        r"\b(I feel [^\.]+ so it must be true)\b",
    ]
}

def categorize_belief(belief: str) -> List[str]:
    matches = []
    for category, patterns in COGNITIVE_DISTORTIONS.items():
        for pattern in patterns:
            if re.search(pattern, belief, flags=re.IGNORECASE):
                matches.append(category)
                break
    return matches or ["Uncategorized"]

def assign_categories_to_beliefs(beliefs: List[BeliefResult]) -> List[BeliefResult]:
    for belief in beliefs:
        belief.categories = categorize_belief(belief.belief)
    return beliefs

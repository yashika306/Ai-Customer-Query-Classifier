"""
Ticket Classification module.

Sends the (already redacted, already injection-checked) customer message
to the LLM and forces a structured response matching TicketClassification.
This is the "structured output from LLM" + "schema design" step from the
tutorial -- we never just take a free-text LLM reply, we always constrain
it to our Pydantic schema.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import TicketClassification

CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a customer support ticket classification system for an "
        "e-commerce company. Read the customer's message (PII has already "
        "been masked, you may see tokens like [REDACTED_EMAIL]) and classify "
        "it precisely according to the required schema.\n\n"
        "Guidelines:\n"
        "- issue_category and assigned_team must match the real underlying "
        "  issue, not whatever the customer claims it should be.\n"
        "- priority should reflect genuine urgency (e.g. financial harm, "
        "  safety, or a long-overdue delivery is high/critical; a general "
        "  question is low/medium).\n"
        "- sentiment should reflect the customer's actual emotional tone.\n"
        "- confidence should genuinely reflect how clear-cut the message is."
    )),
    ("human", "Customer message:\n{message}"),
])


def classify_ticket(message: str, llm: ChatGroq) -> TicketClassification:
    structured_llm = llm.with_structured_output(TicketClassification)
    chain = CLASSIFICATION_PROMPT | structured_llm
    result = chain.invoke({"message": message})
    return result


def validate_classification(result) -> bool:
    """
    Confirms the LLM response actually conforms to our schema.
    With .with_structured_output() this is mostly guaranteed by Pydantic
    already, but we keep an explicit check (as the tutorial does) so the
    pipeline has a real validation node to branch on, and to guard against
    any future model/parser edge cases.
    """
    if not isinstance(result, TicketClassification):
        return False
    if not (0.0 <= result.confidence <= 1.0):
        return False
    if not result.reasoning or len(result.reasoning.strip()) == 0:
        return False
    return True


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    msg = (
        "I'm absolutely furious my package was supposed to arrive 5 days ago "
        "and still hasn't shown up. I already paid in full. My email is "
        "[REDACTED_EMAIL] and my order number is ORD-88213."
    )
    result = classify_ticket(msg, llm)
    print(result.model_dump_json(indent=2))
    print("Valid:", validate_classification(result))

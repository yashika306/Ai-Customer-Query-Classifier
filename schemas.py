"""
Schema definitions for the AI Support Ticket Classifier.

This is the "schema design" step from the tutorial: before talking to the
LLM at all, we define exactly what shape our input and output data take.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal, TypedDict


# ---- Structured output we want FROM the LLM -------------------------------

class TicketClassification(BaseModel):
    """The exact structure we force the LLM to respond in."""

    issue_category: Literal[
        "delivery", "payment", "refund", "product_inquiry",
        "technical_issue", "account_issue", "other"
    ] = Field(description="The category of the customer's issue")

    assigned_team: Literal[
        "logistics", "payments", "customer_support", "technical", "billing"
    ] = Field(description="The team that should handle this ticket")

    priority: Literal["low", "medium", "high", "critical"] = Field(
        description="How urgently this ticket needs to be handled"
    )

    sentiment: Literal["angry", "frustrated", "neutral", "satisfied"] = Field(
        description="The customer's emotional tone"
    )

    confidence: float = Field(
        description="Model's confidence in this classification, 0.0 to 1.0",
        ge=0.0, le=1.0
    )

    reasoning: str = Field(
        description="One sentence explaining why this classification was chosen"
    )


# ---- Internal pipeline state (passed between LangGraph nodes) -------------

class PipelineState(TypedDict, total=False):
    raw_input: str                      # original customer message
    redacted_input: str                 # after PII masking
    pii_detected: list                  # which PII types were found
    injection_detected: bool            # prompt injection flag
    injection_reason: Optional[str]
    classification: Optional[dict]      # the TicketClassification, as dict
    validation_passed: bool
    retry_count: int
    fallback_used: bool
    total_tokens_used: int
    total_cost_usd: float
    final_status: str                   # "success" | "blocked" | "failed"
    error: Optional[str]

"""
Cost Calculator module.

Tracks token usage per LLM call and accumulates session cost. Even though
Groq's free tier has no dollar cost, we still calculate cost using Groq's
published PAID per-token rates -- this is the realistic production pattern:
you track cost as if paying, so you have real guardrails the moment you
scale beyond the free tier (the tutorial's "set a 25-cent cap per user"
example).

Rates below are illustrative per-million-token prices for
llama-3.3-70b-versatile on Groq's paid tier; check console.groq.com/pricing
for current numbers before relying on this for real billing decisions.
"""

PRICING_PER_MILLION_TOKENS = {
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
}

DEFAULT_SESSION_CAP_USD = 0.25


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICING_PER_MILLION_TOKENS.get(
        model, {"input": 0.59, "output": 0.79}  # safe default
    )
    cost = (
        (input_tokens / 1_000_000) * rates["input"]
        + (output_tokens / 1_000_000) * rates["output"]
    )
    return round(cost, 6)


class SessionCostTracker:
    """Accumulates cost/tokens across a whole user session and enforces a cap."""

    def __init__(self, cap_usd: float = DEFAULT_SESSION_CAP_USD):
        self.cap_usd = cap_usd
        self.total_cost = 0.0
        self.total_tokens = 0

    def add_call(self, model: str, input_tokens: int, output_tokens: int) -> float:
        cost = calculate_cost(model, input_tokens, output_tokens)
        self.total_cost += cost
        self.total_tokens += input_tokens + output_tokens
        return cost

    def is_over_cap(self) -> bool:
        return self.total_cost >= self.cap_usd

    def summary(self) -> dict:
        return {
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost, 6),
            "cap_usd": self.cap_usd,
            "over_cap": self.is_over_cap(),
        }


if __name__ == "__main__":
    tracker = SessionCostTracker(cap_usd=0.25)
    tracker.add_call("llama-3.3-70b-versatile", input_tokens=300, output_tokens=120)
    tracker.add_call("llama-3.3-70b-versatile", input_tokens=280, output_tokens=110)
    print(tracker.summary())

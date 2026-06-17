# AI Support Ticket Classifier (LangGraph + Groq)

A production-pattern AI pipeline that classifies customer support tickets
using a free LLM (Groq's Llama 3.3 70B), built with LangGraph. This project
follows the architecture from the "Real AI Engineer Roadmap" tutorial,
implementing the production-quality skills it covers: schema design,
structured LLM output, response validation, prompt injection defense, PII
redaction, retry/fallback handling, and cost tracking.

## Why Groq instead of OpenAI/GPT

The original tutorial uses a paid GPT model. This version swaps in
**Groq**, which offers a genuinely free API tier (no credit card) with
fast inference on open models like Llama 3.3 70B — more than capable for
this classification task, and free to run for learning/portfolio purposes.

## Pipeline architecture

```
customer message
      |
      v
[1] PII Redaction        -- masks credit cards, emails, phone numbers
      |
      v
[2] Injection Check       -- LLM-as-guard: detects prompt injection attempts
      |                       (e.g. "forget all instructions...")
      |-- injection detected --> BLOCKED (ticket not classified)
      v
[3] Classify Ticket       -- structured output via Pydantic schema:
      |                       issue_category, assigned_team, priority,
      |                       sentiment, confidence, reasoning
      v
[4] Validate Response      -- confirms schema compliance
      |-- invalid, retries left --> back to [3]
      |-- invalid, no retries left --> fallback (routes to general queue)
      v
[5] Cost Log               -- tracks tokens + estimated cost per session
      |
      v
   done
```

## Project structure

```
ticket-classifier-ai/
├── app.py                          # Flask server + /classify endpoint
├── graph.py                        # LangGraph pipeline definition
├── schemas.py                      # Pydantic schemas + pipeline state
├── production_modules/
│   ├── pii_redaction.py            # Step 1
│   ├── injection_check.py          # Step 2
│   ├── classifier.py               # Step 3 + 4
│   └── cost_calculator.py          # Step 5
├── static/
│   └── index.html                  # Browser UI (security-console style)
├── requirements.txt
├── .env.example                    # Copy to .env, add your Groq key
└── README.md
```

## Setup (Windows / VS Code)

1. **Get a free Groq API key** (no credit card required):
   - Go to https://console.groq.com/keys
   - Sign up / log in, click "Create API Key", copy it

2. **Open this project folder in VS Code**, then in the terminal:

   ```powershell
   pip install -r requirements.txt
   ```

3. **Add your API key:**
   - Copy `.env.example` to a new file named `.env` in the same folder
   - Open `.env` and paste your key:
     ```
     GROQ_API_KEY=gsk_your_actual_key_here
     ```

4. **Run the web app:**

   ```powershell
   python app.py
   ```

   Then open **http://127.0.0.1:5000** in your browser. Try the example
   buttons (a normal angry complaint with PII, a prompt injection attempt,
   and a calm low-priority question) to see all four pipeline stages light
   up in real time.

   Alternatively, run the pipeline directly from the terminal without the
   UI:

   ```powershell
   python graph.py
   ```

   This runs two built-in test cases and prints the full pipeline state
   for each, including PII detected, injection detection, classification,
   and running cost.

## Testing individual modules

Each production module can also be run standalone to see just that
piece in isolation:

```powershell
python production_modules/pii_redaction.py      # no API key needed
python production_modules/injection_check.py    # needs GROQ_API_KEY
python production_modules/classifier.py         # needs GROQ_API_KEY
python production_modules/cost_calculator.py     # no API key needed
```

## Notes on Groq's free tier

As of mid-2026, Groq's free tier for `llama-3.3-70b-versatile` allows
roughly 30 requests/minute and 1,000 requests/day with no cost and no
credit card. That's far more than enough for development, testing, and
demoing this project. If you ever hit a `429` rate-limit error, just wait
a minute and retry — the limit resets on a rolling window.

## Honest notes for interviews

- **Cost tracking is illustrative, not exact.** Token counts are
  estimated (Groq's structured-output response doesn't always expose
  precise usage through this LangChain interface), and the per-token
  rates used are Groq's *paid*-tier rates, even though you're on the free
  tier — this mirrors the real production habit of costing your free
  usage as if it weren't free, so you have guardrails the moment you scale.
- **The injection guard is an LLM itself**, which means it isn't
  perfect — sufficiently creative attacks can sometimes slip through, and
  legitimate urgent messages can occasionally be over-flagged. Production
  systems typically combine this with rule-based checks (e.g. flagging
  literal phrases like "ignore previous instructions") for defense in
  depth.
- **PII redaction here is regex-based**, which is fast and free but will
  miss PII that doesn't match the patterns (e.g. unusual phone formats,
  non-US formats). A production system would likely add a dedicated PII
  detection model or service for better recall.

## Possible extensions

- Add rule-based keyword detection alongside the LLM injection guard
- Swap the regex PII redaction for a proper NER-based PII detector
- Add a real per-user session cost cap that blocks further requests once hit
- Persist classified tickets to a database with a simple dashboard
- Add automated tests comparing classifier output against labeled examples

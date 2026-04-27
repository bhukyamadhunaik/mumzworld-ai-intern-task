# Mumzworld Smart Gift Finder & Advisor

**Track:** A (AI Engineering Intern)

### Summary
The **Smart Gift Finder & Advisor** is an AI-powered shopping assistant for Mumzworld customers, specifically designed for gift-buyers (e.g., friends, relatives, or busy parents) who need thoughtful, budget-aware, and age-appropriate recommendations in both English and Arabic. It takes a free-text natural language query, extracts relevant constraints (budget, child's age, interests), queries a mock product catalog using Agentic Tool Calling, and synthesizes a curated list of recommendations with personalized reasoning validated against a strict Pydantic JSON schema.

---

### Setup and Run Instructions

This project takes under 3 minutes to run.

1. **Clone the repo** (or navigate to the project directory).
2. **Set up a virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Set your API Keys**:
   This project uses standard OpenAI API format but is designed to run with **OpenRouter** (as recommended for free access to models like Llama 3.3 70B).
   ```bash
   export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
   export OPENAI_API_KEY="sk-or-v1-..."  # Replace with your OpenRouter API key
   export MODEL_NAME="meta-llama/llama-3.3-70b-instruct" # Optional, defaults to gpt-4o-mini if not set
   ```
   *Windows users: Use `set` instead of `export`.*

4. **Run the prototype**:
   ```bash
   python -m src.agent
   ```
   *(This will run a quick built-in test case).*

5. **Run the evals**:
   ```bash
   pytest evals/eval_gift_finder.py -v
   ```

---

### Tooling Transparency
* **Harnesses & Models Used**: I used standard `openai` python package configured to hit **OpenRouter** APIs, specifically targeting models like `meta-llama/llama-3.3-70b-instruct` or `google/gemini-2.5-flash-api` which have excellent tool-calling and JSON formatting capabilities.
* **How I used AI**: I used Google's Agentic AI framework (Antigravity) as a pair-programmer to scaffold the boilerplate (directory structure, mock JSON generation, basic Pydantic schemas). 
* **What worked / didn't work**: Relying purely on the model to "know" product details hallucinated fake products. Stepping in to enforce **Tool Calling** (querying a local `catalog.json` mock database) completely eliminated product hallucinations. The LLM handles the extraction and formatting, while the deterministic code handles the search logic.
* **System Prompting**: The key prompt used forces the LLM to output pure JSON matching the Pydantic schema and demands explicit reasoning in both English and Arabic. See `src/agent.py` for the exact prompt injection.

---
*Note: This repository contains the code for the Track A submission. Please refer to `EVALS.md` and `TRADEOFFS.md` for the deeper engineering analysis.*

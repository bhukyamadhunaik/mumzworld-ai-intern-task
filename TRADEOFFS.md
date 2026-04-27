# Architecture & Tradeoffs

### Why this problem? (And what I rejected)
I selected the **Smart Gift Finder & Advisor** because it perfectly hits the intersection of high business value and non-trivial AI engineering. Gift buying is a high-friction user journey. Buyers often don't know what a 6-month-old needs versus a 3-year-old, leading to abandoned carts. 

**What I rejected:**
* *Pediatric Symptom Triage:* Too much medical liability risk. An e-commerce platform shouldn't play doctor.
* *Return Reason Classification:* Easy to build with a single zero-shot classification prompt, but low impact compared to top-of-funnel conversion tools like a Gift Finder.

### Architecture & Model Choice
* **Pattern:** Agentic Tool-Calling + Structured Output Validation.
* **Why not simple RAG?** RAG (vector search over all products) is great, but budget and age constraints are *hard filters*. If I have 150 AED, recommending a 200 AED item is a terrible user experience, regardless of cosine similarity. By using Tool Calling, the LLM extracts the hard variables (budget = <150, age = 12m), queries the deterministic API tool, and then uses its "soft reasoning" to select the best 3 out of the returned valid pool.
* **Model:** Llama 3.3 70B (or GPT-4o-mini). These models have phenomenal JSON-mode structured output capabilities and follow system instructions strictly, which is required to bind output to Pydantic schemas.

### How I Handled Uncertainty
The hallmark of a bad AI product is confidence in hallucination.
1. **Catalog Grounding:** The model is not allowed to invent products. It *must* use the `search_catalog` tool. If the tool returns `[]` (e.g., for an impossibly low budget of 5 AED), the model is prompted to synthesize a polite "I don't know / I couldn't find anything" response rather than making up a 5 AED stroller.
2. **Schema Enforcement:** Pydantic is used to wrap the output. If the model outputs broken JSON or misses a required field (like `reasoning_ar`), the backend throws an explicit `ValidationError` rather than silently failing on the frontend.

### What I Cut (Scope constraints)
1. **Embeddings/Vector Search:** For the mock catalog search, I used a naive Python string-match and list comprehensions to save time. In a real environment, `search_catalog` would query Pinecone/Weaviate for semantic matching combined with metadata filtering for price/age.
2. **Frontend UI:** I built the core AI engineering backend logic. Connecting this to a Next.js/React frontend with streaming JSON was cut to stay within the 5-hour limit and focus purely on AI rigor.

### What I Would Build Next
1. **Streaming JSON:** Wrapping the Pydantic parser in an iterative JSON stream (using something like `jiter`) so the UI can show the products loading one by one, rather than waiting 4 seconds for the full API response.
2. **A/B Testing Copy Quality:** Implement an LLM-as-a-judge specifically calibrated with Mumzworld's brand voice guidelines to automatically grade the Arabic and English generated reasoning in staging before deployment.

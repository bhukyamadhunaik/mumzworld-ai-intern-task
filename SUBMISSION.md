# Mumzworld AI Engineering Intern (Track A) Submission

**1. Track:** A (AI Engineering Intern)

**2. Summary:** 
I built the **Smart Gift Finder & Advisor**, an AI-powered shopping assistant designed for friends, relatives, or busy parents shopping on Mumzworld. It takes a natural-language query (in English or Arabic), extracts constraints like budget and the child's age, and uses Agentic Tool Calling to search a mock product catalog. It then synthesizes a curated list of recommendations with personalized, translated reasoning, strictly validating the output against a Pydantic schema to guarantee reliability.

**3. Prototype Access:**
* **GitHub Repository:** [Insert your GitHub Repo Link Here]
* **Setup Instructions:** Please see the `README.md` in the repository for instructions on how to run the prototype locally in under 3 minutes using OpenRouter.

**4. Walkthrough Loom:**
[Insert your Loom link here]

**5. Markdown Deliverables:**
* Please find `EVALS.md` and `TRADEOFFS.md` in the root of the GitHub repository.

**6. AI Usage Note:**
I used standard `openai` Python tools configured for OpenRouter to access Llama-3.3-70B-Instruct for high-quality tool calling and structured JSON output. I partnered with an AI Coding Assistant (Antigravity) to scaffold the repository, generate the mock product JSON, and write the Pydantic schema boilerplates. I manually designed the agentic loops, the evaluation rubric, and the architectural tradeoffs to ensure deterministic tool search combined with LLM semantic reasoning.

**7. Time Log:**
* Problem Ideation & Architecture: 1 hour
* Mock Data & Tool Creation: 1 hour
* Agent Loop & Prompt Engineering: 1.5 hours
* Evals, Testing, and Edge-Case Handling: 1 hour
* Documentation & Loom Recording: 0.5 hours
*(Total: ~5 hours)*

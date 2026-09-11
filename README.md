# SmartRecipe AI — RAG-Based Recipe Preparation Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SmartRecipe AI** helps users cook a meal using ingredients they already
have. It retrieves the closest matching recipe from a curated knowledge base
(Retrieval-Augmented Generation) and uses an **IBM Granite** model to turn it
into a personalized, step-by-step cooking guide — complete with dietary
adaptation, ingredient substitutions, and automatic serving-size scaling.

Built for **AICTE 2026 — Problem Statement No. 16: Recipe Preparation
Agent**, as part of the IBM SkillsBuild / Edunet Foundation University
Engagement Program.

> Live demo: build the flow in Langflow following [`docs/SETUP.md`](docs/SETUP.md).

---

## Why this project

Home cooks routinely discard usable food simply because they don't know what
to make with what's on hand. Generic recipe search demands exact ingredient
matches and ignores dietary restrictions. SmartRecipe AI starts from the
opposite direction — **what do you have, right now** — and builds a real,
cookable recipe around it.

## Core features

1. Ingredient-based recipe recommendations
2. Recipe retrieval from a knowledge base (RAG)
3. Dietary preference handling (vegetarian / vegan / gluten-free / non-vegetarian)
4. Missing-ingredient substitutions
5. Serving-size adjustment (automatic ingredient scaling)
6. Step-by-step cooking instructions
7. Cooking tips
8. Beginner-friendly, friendly-toned responses

The project is intentionally scoped to stay lightweight — no voice
assistant, no image recognition, no mobile app, no auth/payment systems, no
extra databases or dashboards, no multi-agent complexity, and no external
APIs beyond IBM watsonx.ai. See [`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md)
for the full rationale.

## Architecture (short version)

```
User → Langflow Chat Input → Recipe Retrieval (RAG over recipes.csv)
     → Prompt Construction (system_prompt.txt + retrieved recipe + scaled
       ingredients) → IBM Granite (via watsonx.ai) → Langflow Chat Output
```

Full diagram and component breakdown: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
RAG design details: [`docs/RAG_PIPELINE.md`](docs/RAG_PIPELINE.md).

## Repository structure

```
SmartRecipe-AI/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── requirements.txt
├── app.json                    <- exported Langflow flow
├── system_prompt.txt           <- SmartRecipe AI persona instructions
├── scale_recipe.py             <- ingredient scaling utility
├── recipe_agent_local.py       <- local, no-API-call reference implementation
├── data/
│   └── recipes.csv             <- curated recipe knowledge base
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RAG_PIPELINE.md
│   ├── SETUP.md
│   └── PROJECT_REPORT.md
└── .gitignore
```

## Quick start (no coins, no API key needed)

```bash
git clone https://github.com/<your-username>/SmartRecipe-AI.git
cd SmartRecipe-AI
pip install -r requirements.txt
python recipe_agent_local.py
```

This runs the full retrieval → dietary filter → substitution check → serving
scale → prompt-building pipeline locally, so you can verify everything works
before spending any watsonx.ai or Bobcoin credits. See
[`docs/SETUP.md`](docs/SETUP.md) for wiring it up in Langflow with IBM
Granite.

## Technology used

- **IBM Granite** (via IBM watsonx.ai) — recipe reasoning and generation
- **Langflow** — visual, low-code agent orchestration
- **IBM Cloud Lite** — hosting infrastructure
- **Python / pandas** — the local reference implementation and retrieval logic
- **IBM Bob** — used for one focused code-review task on `scale_recipe.py` (see `docs/PROJECT_REPORT.md`)

## Contributing

Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md) and
please follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Security

Found a security issue? Please see [`SECURITY.md`](SECURITY.md) for how to
report it responsibly.

## License

MIT — see [`LICENSE`](LICENSE).

---
*Submitted as part of the AICTE–IBM SkillsBuild–Edunet Foundation
University Engagement Program, 2026.*

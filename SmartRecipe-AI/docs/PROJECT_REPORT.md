# Project Report

## Problem Statement

**AICTE 2026 — Problem Statement No. 16: Recipe Preparation Agent (RAG-Based)**

> A Recipe Preparation Agent helps users cook meals using only the
> ingredients they have on hand, using a RAG-based AI system to retrieve
> relevant recipes and generate step-by-step instructions adapted to
> ingredient limitations, with substitutions, cooking tips, and dietary
> adjustments.
> **Technology:** Use of IBM Cloud Lite services / IBM Granite is mandatory.

## Solution Summary

SmartRecipe AI implements this as a single Langflow flow: a user's
available ingredients and preferences are matched against a curated recipe
knowledge base (RAG), the matched recipe's quantities are scaled to the
requested serving size, and an IBM Granite model (via IBM watsonx.ai)
generates the final structured, beginner-friendly recipe response.

## Scope decisions and rationale

The project deliberately excludes several features that would add
complexity without adding proportional value for a small, single-flow
student project:

| Excluded | Why |
|---|---|
| Voice assistant | Adds a whole additional I/O layer for a text-first chat use case |
| Image recognition | Requires multimodal infrastructure beyond what's needed for the core RAG flow |
| Mobile application | Langflow's chat interface / any simple web frontend is sufficient for a demo |
| Authentication / payments | Not relevant — this is a stateless recipe assistant, not a commercial product |
| Additional databases / dashboards | The recipe knowledge base is small enough that a CSV + Langflow is sufficient |
| Multi-agent complexity | A single flow with one model call is easier to build, debug, and explain |
| External APIs beyond watsonx.ai | Keeps the dependency surface small and the project easy to run |

These are documented here so future contributors (or graders) understand
they were intentional scope decisions, not oversights — and each is a
reasonable direction for **Future Work** if the project continues.

## Role of IBM Bob

IBM Bob (an AI coding assistant) was used for a single, focused task:
reviewing `scale_recipe.py` for correctness — specifically, confirming it
handles ingredients with non-numeric quantities (e.g. "a pinch of salt")
without crashing, and suggesting any refinement. This kept Bobcoin usage
minimal (a handful of coins, well under the 20-coin target) while still
providing genuine, verifiable evidence of using the tool as required by the
assignment.

## Role of IBM Granite / watsonx.ai

IBM Granite, accessed via IBM watsonx.ai, is the model used inside the
Langflow flow's Model component. It receives the system prompt (persona +
response format) and the retrieved, scaled recipe context, and generates
the final natural-language recipe response shown to the user.

## Future Work

- Regional cuisine expansion (more recipes, cuisine-specific modules)
- Multilingual support for non-English-speaking users
- Photo-based pantry detection using multimodal Granite models
- Grocery-list generation for missing ingredients

## Team / Submission

- Problem Statement: No. 16 — Recipe Preparation Agent (RAG-Based)
- Technology: Langflow, IBM Granite, IBM watsonx.ai, IBM Cloud Lite, IBM Bob
- Repository: add your GitHub URL here after pushing

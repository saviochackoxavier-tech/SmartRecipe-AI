# Setup Guide

## Part 1 — Test the logic locally (free, no coins)

```bash
git clone https://github.com/<your-username>/SmartRecipe-AI.git
cd SmartRecipe-AI
pip install -r requirements.txt
python recipe_agent_local.py
```

Try a few inputs (e.g. `rice, onion, egg` / `vegetarian` / `3`) and confirm
the printed prompt looks correct — this is exactly what will be sent to IBM
Granite once the flow is live in Langflow.

## Part 2 — Build the flow in Langflow

1. **Create a new flow** in Langflow.
2. Add a **Chat Input** component.
3. Add a **File Loader** component pointed at `data/recipes.csv`.
4. Add a **Custom Component** and paste in the contents of `scale_recipe.py`.
5. Add a **Prompt Template** component. Set the system message to the full
   contents of `system_prompt.txt`, and template the user turn using the
   retrieved recipe + scaled ingredients (see `build_prompt()` in
   `recipe_agent_local.py` for the exact structure to replicate).
6. Add an **IBM watsonx.ai Model** component:
   - Connect your watsonx.ai project and API key.
   - Select an **IBM Granite** model (e.g. `granite-3-8b-instruct` or
     `granite-4.0-8b-instruct`).
7. Add a **Chat Output** component.
8. Connect the components in this order:
   `Chat Input → File Loader + Custom Component → Prompt Template → IBM watsonx.ai Model → Chat Output`
9. **Test** in the Langflow Playground with 2–3 sample inputs.
10. **Export**: Langflow → Export → save as `app.json`, replacing the
    placeholder in this repo.

## Part 3 — (Optional) Use IBM Bob efficiently

If your task requires demonstrating IBM Bob usage, do **one small, focused**
task rather than asking it to generate the whole project (which wastes
coins and produces code you still have to review anyway):

> "Review `scale_recipe.py`. Confirm it handles an ingredient with no
> numeric quantity (like 'a pinch of salt') without crashing, and suggest
> one small improvement."

Take a screenshot of that single exchange — it's genuine evidence of using
the tool, and costs only a few coins.

## Part 4 — Push to GitHub

```bash
git init
git add .
git commit -m "SmartRecipe AI - AICTE IBM SkillsBuild project"
git branch -M main
git remote add origin https://github.com/<your-username>/SmartRecipe-AI.git
git push -u origin main
```

Confirm the repo is **public**, has its **README rendering correctly**, and
contains `app.json`, your problem-statement PDF, and your final `.pptx`.

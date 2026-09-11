# Security Policy

## Supported Version

This is a student project built for AICTE 2026 / IBM SkillsBuild. The
`main` branch is the only supported version.

## Reporting a Vulnerability

This project does not process payments, store personal user accounts, or
handle sensitive personal data — it's a recipe-suggestion agent that reads
a local CSV file and calls the IBM watsonx.ai API.

If you still find a security concern (for example, a way to leak API
credentials, or an injection issue in how user input is passed to the
model), please open a GitHub Issue describing the problem, or contact the
repository maintainer directly rather than disclosing it publicly if it's
sensitive.

## Handling credentials

- Never commit your IBM watsonx.ai API key or project ID to this
  repository. Use environment variables or Langflow's built-in credential
  storage instead.
- The included `.gitignore` excludes `.env` files for this reason — keep
  your real credentials there, not in tracked files.

# Deployment Guide

This project is prepared for deployment with Render using the included `render.yaml`.

## What Gets Deployed

- `disaster-forecast-api`
  Runs the FastAPI backend
- `disaster-forecast-ui`
  Runs the Streamlit frontend

The UI reads the backend address from the `API_URL` environment variable.

## Deploy On Render

1. Push this repository to GitHub.
2. Log in to Render.
3. Choose `New +` -> `Blueprint`.
4. Connect your GitHub repository.
5. Select this repository and deploy.
6. Render will create both services from `render.yaml`.

## After Deploy

- The API will get a public URL similar to:
  `https://disaster-forecast-api.onrender.com`
- The UI will get a public URL similar to:
  `https://disaster-forecast-ui.onrender.com`

Use the UI URL as your application link for submission.

## Important Notes

- In this repository, the app is stable even if no local base model is available.
- If you want the full adapted model response instead of fallback behavior, provide a local compatible base model path through environment configuration.
- Snowflake is optional. If credentials are missing, the app falls back to sample warehouse facts.

## Local Alternative

If you only need screenshots and not a public app link, run locally:

```bash
uvicorn api:app --reload
streamlit run app.py
```

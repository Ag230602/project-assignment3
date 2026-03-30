# Railway Deployment Guide

This project can be deployed on Railway as two services from the same repository:

- FastAPI backend service
- Streamlit frontend service

## 1) Deploy Backend (FastAPI)

1. In Railway, create a new service from this GitHub repository.
2. Set **Root Directory** to `Lab8_Individual_Submission_Adrija`.
3. Set **Start Command**:

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

4. Deploy and copy the generated public URL.
5. Verify:

```bash
https://<backend-url>/healthz
```

## 2) Deploy Frontend (Streamlit)

1. Create another Railway service from the same repository.
2. Set **Root Directory** to `Lab8_Individual_Submission_Adrija`.
3. Set **Start Command**:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

4. Add environment variable:

- `API_URL=https://<backend-url>`

5. Deploy and open the frontend public URL.

## Optional Procfile Templates

This repo includes:

- `Procfile.api`
- `Procfile.ui`

Use them as command references for the two Railway services.

## Troubleshooting

- If frontend cannot connect, confirm `API_URL` points to backend URL (not localhost).
- Confirm backend `/healthz` returns JSON and status 200.
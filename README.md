# Mini University AI Assistant

A very small learning project for understanding **Python + FastAPI** before adding:

- LLM integration
- RAG
- AI Agents
- MCP

## 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Run the server

```powershell
uvicorn app.main:app --reload
```

## 4. Open in browser

Home:

```text
http://127.0.0.1:8000/
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## Current endpoints

- `GET /`
- `POST /ask`

Example request body for `/ask`:

```json
{
  "question": "What is RAG?"
}
```

At this stage, `/ask` returns a placeholder answer.
We will connect a real LLM in the next step.

# AI API Failure Detective

An MVP that analyzes API incidents using FastAPI, LangGraph, and Azure OpenAI.

## Setup

```powershell
uv sync
```

Create a `.env` file:

Run the API from the project root:

```powershell
uv run uvicorn --app-dir App main:app --reload
```

Open `http://127.0.0.1:8000` in a browser.

## API

- `GET /api/incidents` - list incidents
- `GET /api/incidents/{incident_id}` - get an incident
- `POST /api/incidents/{incident_id}/investigate` - analyze an incident
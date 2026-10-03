from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from data import INCIDENTS
from agent import graph


app = FastAPI(
    title="AI API Failure Detective",
    description="AI-powered API incident investigation MVP",
    version="0.1.0"
)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/api/incidents")
def get_incidents():
    return INCIDENTS


@app.get("/api/incidents/{incident_id}")
def get_incident(incident_id: str):

    for incident in INCIDENTS:

        if incident["id"] == incident_id:
            return incident

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )


@app.post("/api/incidents/{incident_id}/investigate")
def investigate(incident_id: str):

    incident = None

    for item in INCIDENTS:

        if item["id"] == incident_id:
            incident = item
            break

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    result = graph.invoke({
        "incident": incident,
        "analysis": {}
    })

    return {
        "incident": result["incident"],
        "analysis": result["analysis"]
    }


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
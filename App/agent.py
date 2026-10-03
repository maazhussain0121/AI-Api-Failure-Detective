import json
import os
from typing import Any, TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr


load_dotenv()


class IncidentState(TypedDict):
    incident: dict
    analysis: dict


# Get API key
api_key = os.getenv("AZURE_OPENAI_API_KEY")

if not api_key:
    raise ValueError("AZURE_OPENAI_API_KEY is not set in .env")


# Azure OpenAI LLM
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=SecretStr(api_key),
    azure_deployment=os.getenv("AZURE_CHAT_MODEL_DEPLOYMENT"),
    api_version=os.getenv(
        "AZURE_OPENAI_API_VERSION",
        "2024-10-21"
    ),
    temperature=0,
)


def get_text(content: Any) -> str:
    """
    Convert LangChain message content into plain text.
    Handles both string and structured/list content.
    """

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):
                if "text" in item:
                    parts.append(str(item["text"]))
                else:
                    parts.append(str(item))

            else:
                parts.append(str(item))

        return "\n".join(parts)

    return str(content)


def investigate_incident(state: IncidentState):

    incident = state["incident"]

    logs = "\n".join(incident["logs"])

    prompt = f"""
        You are an AI API Failure Detective.

        Analyze the following API incident.

        IMPORTANT:
        - Only use evidence present in the incident.
        - Do not invent logs, metrics, services, or events.
        - Clearly distinguish facts from your hypothesis.
        - Identify the most likely root cause.
        - Explain the failure chain.

        INCIDENT:

        Incident ID:
        {incident["id"]}

        Endpoint:
        {incident["endpoint"]}

        HTTP Status:
        {incident["status_code"]}

        Service:
        {incident["service"]}

        Timestamp:
        {incident["timestamp"]}

        Request Duration:
        {incident["duration_ms"]} ms

        LOGS:
        {logs}

        Return ONLY valid JSON using this structure:

        {{
            "summary": "short explanation",
            "affected_service": "service name",
            "root_cause": "most likely root cause",
            "confidence": "High/Medium/Low",
            "failure_chain": [
                "step 1",
                "step 2",
                "step 3"
            ],
            "evidence": [
                "evidence 1",
                "evidence 2"
            ],
            "recommendations": [
                "recommendation 1",
                "recommendation 2"
            ]
        }}"""

    response = llm.invoke(prompt)

    content = get_text(response.content).strip()

    if "```json" in content:
        content = content.replace("```json", "").replace("```", "").strip()

    elif "```" in content:
        content = content.replace("```", "").strip()

    try:
        analysis = json.loads(content)

    except json.JSONDecodeError:

        analysis = {
            "summary": content,
            "affected_service": incident["service"],
            "root_cause": "Unable to parse structured response",
            "confidence": "Low",
            "failure_chain": [],
            "evidence": [],
            "recommendations": []
        }

    return {
        "incident": incident,
        "analysis": analysis
    }



graph_builder = StateGraph(IncidentState)

graph_builder.add_node(
    "investigate",
    investigate_incident
)

graph_builder.add_edge(
    START,
    "investigate"
)

graph_builder.add_edge(
    "investigate",
    END
)

graph = graph_builder.compile()
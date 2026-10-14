from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import requests
import tempfile
import os
import json

from fastapi.responses import FileResponse

from app.tools import calculator
from mcp_client import call_mcp_tool, list_mcp_tools
from app.rag import read_pdf, split_text, create_embedding, find_best_chunks

app = FastAPI(
    title="Mini University AI Assistant",
    version="0.1.0",
)

@app.get("/")
def frontend():
    return FileResponse("frontend/index.html")


document_chunks = []
document_embeddings = []


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Mini University AI Assistant is running"}


@app.post("/ask")
async def ask_question(data: QuestionRequest):

    # Get MCP tools automatically from the MCP Server
    mcp_tools = await list_mcp_tools()

    # Extract only tool names
    mcp_tool_names = [tool["name"] for tool in mcp_tools]

    # Convert tools + descriptions into text for Qwen
    mcp_tools_text = "\n".join(
        f'- {tool["name"]}: {tool["description"]}' for tool in mcp_tools
    )

    # Ask Qwen to choose the correct tool
    decision_prompt = f"""
You are an AI agent.

Choose the correct tool for the user's question.

Local tools:
- calculator: use for mathematical calculations
- rag: use for questions about the uploaded document

MCP tools:
{mcp_tools_text}

Return ONLY valid JSON in this format:

{{
  "tool": "tool name",
  "reason": "short reason"
}}

Question:
{data.question}
"""

    decision_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:4b",
            "prompt": decision_prompt,
            "stream": False,
        },
    )

    decision_result = decision_response.json()

    decision = json.loads(decision_result["response"])

    tool_choice = decision["tool"]
    reason = decision["reason"]

    # Local Calculator Tool
    if tool_choice == "calculator":
        answer = calculator(data.question)

        return {
            "question": data.question,
            "tool_used": "calculator",
            "reason": reason,
            "answer": answer,
        }

    # Dynamic MCP Tool
    if tool_choice in mcp_tool_names:
        answer = await call_mcp_tool(tool_choice)

        return {
            "question": data.question,
            "tool_used": tool_choice,
            "reason": reason,
            "answer": answer,
        }

    # Local RAG Tool
    if tool_choice == "rag":

        if not document_chunks:
            return {"error": "Please upload a PDF first."}

        top_chunks = find_best_chunks(
            data.question, document_chunks, document_embeddings, top_k=3
        )

        context = "\n\n---\n\n".join(chunk for chunk, score in top_chunks)

        prompt = f"""
You are a university assistant.

Answer the user's question using ONLY the context below.

Context:
{context}

Question:
{data.question}

If the answer cannot be found in the context,
say: "I don't have enough information."
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3:4b",
                "prompt": prompt,
                "stream": False,
            },
        )

        result = response.json()

        return {
            "question": data.question,
            "tool_used": "rag",
            "reason": reason,
            "answer": result["response"],
        }

    return {"error": "Unknown tool selected."}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:

        temp_file.write(await file.read())

        temp_path = temp_file.name

    text = read_pdf(temp_path)

    chunks = split_text(text)

    embeddings = [create_embedding(chunk) for chunk in chunks]

    global document_chunks
    global document_embeddings

    document_chunks = chunks
    document_embeddings = embeddings

    os.remove(temp_path)

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks_count": len(chunks),
        "first_chunk": chunks[0] if chunks else "",
    }

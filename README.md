# Raheem AI Assistant

A local agentic AI assistant built with **Python, FastAPI, Qwen, Ollama, RAG, and MCP**.

The project demonstrates how a Large Language Model can analyze a user's request, select the appropriate tool, retrieve information from documents, and interact with tools exposed through the Model Context Protocol.

---

## Overview

Raheem AI Assistant is a small AI engineering project created to explore the core concepts behind modern AI-powered applications.

The assistant can:

- Answer questions using a local LLM.
- Upload and process PDF documents.
- Retrieve relevant document content using RAG.
- Generate embeddings and perform similarity search.
- Select the appropriate tool based on the user's question.
- Execute local tools.
- Discover and execute MCP tools dynamically.
- Run locally without requiring a paid LLM API.

---

## Architecture

```text
                         User
                          │
                          ▼
                     Frontend
                          │
                          ▼
                     FastAPI
                          │
                          ▼
                      Qwen LLM
                          │
                    Tool Selection
                 ┌────────┼────────┐
                 │        │        │
                 ▼        ▼        ▼
                RAG   Local Tool   MCP
                 │                 │
                 │            MCP Client
                 │                 │
                 │            MCP Server
                 │                 │
                 ▼                 ▼
             PDF Search           Tools
                 │                 │
                 └────────┬────────┘
                          ▼
                     Final Answer
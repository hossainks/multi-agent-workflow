# Multi-Agent Workflow — Automated User Registration Pipeline

A production-style, AI-driven automation pipeline that chains three specialized agents to execute a complete end-to-end user registration workflow: **database retrieval → API testing → Excel reporting**. Built on Microsoft AutoGen and the Model Context Protocol (MCP).

---

## What It Does

This workflow automates a real-world QA/testing scenario:

1. **Pulls** a random user record from a live MySQL database
2. **Constructs** a valid registration request and calls the registration API
3. **Logs in** with the registered credentials and verifies the response
4. **Records** successful results into an Excel report — only if login truly succeeded

All three steps are carried out by autonomous AI agents that each hold only the tools they need and communicate by passing structured data through natural language messages.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        agents.py  (entry point)                     │
│                                                                     │
│   OpenAIChatCompletionClient (gpt-5-mini)                           │
│          │                                                          │
│          ▼                                                          │
│   AgentAgency (factory)                                             │
│     ├── create_database_agent()                                     │
│     ├── create_api_agent()                                          │
│     └── create_excel_agent()                                        │
│                                                                     │
│   RoundRobinGroupChat ──► TextMentionTermination                    │
│     │           ("REGISTRATION PROCESS COMPLETE")                  │
│     ▼                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ DatabaseAgent│───►│   ApiAgent   │───►│  ExcelAgent  │          │
│  │              │    │              │    │              │          │
│  │ MCP: MySQL   │    │ MCP: REST API│    │ MCP: Excel   │          │
│  │              │    │ MCP: FS      │    │              │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

### Agent Handoff Protocol

Agents coordinate through **structured signal phrases** embedded in their chat messages — no shared state object, no message bus:

| Step | Agent | Writes to chat | Triggers |
|------|-------|----------------|----------|
| 1 | `DatabaseAgent` | `DATABASE_DATA_READY → APIAgent should proceed next` | ApiAgent starts |
| 2 | `ApiAgent` | `API_TESTING_COMPLETE → Excel Agent should ...` | ExcelAgent starts |
| 3 | `ExcelAgent` | `REGISTRATION PROCESS COMPLETE` | Loop terminates |

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Agent orchestration | [Microsoft AutoGen](https://github.com/microsoft/autogen) (`autogen_agentchat`, `autogen_ext`) |
| Tool integration | [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) via `McpWorkbench` |
| LLM backend | OpenAI (`gpt-5-mini`) via `OpenAIChatCompletionClient` |
| Database | MySQL (via `@benborla29/mcp-server-mysql`) |
| HTTP client | REST API MCP server (`dkmaker-mcp-rest-api`) |
| File I/O | Excel MCP (`@negokaz/excel-mcp-server`), Filesystem MCP (`@modelcontextprotocol/server-filesystem`) |
| Runtime | Python 3.x + `asyncio` |

---

## Key Design Decisions

**MCP over custom tool code** — Every external integration (database, HTTP, Excel, filesystem) is wired up as an MCP server launched via `npx`. This means zero integration boilerplate in Python; agents receive a `McpWorkbench` and the LLM decides how to call the tools.

**Least-privilege tool access** — Each agent is given only the workbenches it needs. `DatabaseAgent` has MySQL only. `ApiAgent` has REST API + filesystem (to read the Postman collection). `ExcelAgent` has Excel only. This prevents agents from accidentally using tools outside their scope.

**Conditional write gate** — `ExcelAgent` checks whether login actually succeeded before writing to the spreadsheet. This is enforced in the system message: no successful login → no Excel row written.

**`AgentAgency` factory pattern** — Agent creation is separated from orchestration. `AgentAgency` takes a model client and exposes typed factory methods, making it straightforward to swap models or add new agent types without touching `agents.py`.

---

## Project Structure

```
multi-agent-workflow/
├── agents.py          # Entry point — builds agents, team, runs the workflow
├── agentagency.py     # AgentAgency factory class
├── mcpconfig.py       # McpConfig — static factory methods for each MCP workbench
├── .env               # Runtime secrets (never committed)
└── .venv/             # Python virtual environment
```

---

## Prerequisites

- Python 3.10+
- Node.js 18+ with `npx` available on PATH (used to auto-install MCP servers at runtime)
- A running MySQL instance with the `rahulshettyacademy` database
- An OpenAI API key

---

## Setup

**1. Clone and create the virtual environment**

```bash
git clone <repo-url>
cd multi-agent-workflow
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
```

**2. Install dependencies**

```bash
pip install autogen-agentchat autogen-ext[openai,mcp] python-dotenv
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=your_db_user
MYSQL_PASS=your_db_password
MYSQL_DB=your_database
```

**4. Place your Postman collection**

Put the JSON collection file(s) in:
```
C:\Users\<you>\Desktop\Claude-Test\Json-Files\
```
The `ApiAgent` reads these at runtime to understand the API contract before making calls.

---

## Running the Workflow

```bash
python agents.py
```

The AutoGen `Console` streams each agent's output to the terminal in real time. The process exits automatically when `ExcelAgent` writes `REGISTRATION PROCESS COMPLETE`.

---

## Workflow In Detail

```
agents.py
   │
   ├─► DatabaseAgent
   │     ├── Connects to MySQL via MCP
   │     ├── Queries RegistrationDetails table (random record)
   │     ├── Queries Usernames table (additional data)
   │     ├── Merges records + ensures email uniqueness (timestamp suffix)
   │     └── Emits structured REGISTRATION_DATA block → signals ApiAgent
   │
   ├─► ApiAgent
   │     ├── Reads Postman collection from filesystem (MCP)
   │     ├── Extracts API contract (endpoint, required fields)
   │     ├── Constructs request body from DatabaseAgent's data
   │     │     email    → from DB + unique timestamp
   │     │     password → SecurePass123 format
   │     │     mobile   → 10-digit format
   │     ├── POST /register — proceeds even on "user already exists"
   │     ├── POST /login    — with same credentials
   │     └── Reports success/failure → signals ExcelAgent
   │
   └─► ExcelAgent
         ├── Reads registration data from DatabaseAgent's message
         ├── Reads login result from ApiAgent's message
         ├── Skips write if login failed (conditional guard)
         ├── Opens devdata.xlsx via MCP, appends row with timestamp
         └── Saves file → writes "REGISTRATION PROCESS COMPLETE"
```

---

## Extending the Workflow

To add a new agent:

1. Add a `get_<tool>_workbench()` static method to `McpConfig` in `mcpconfig.py`
2. Add a `create_<role>_agent()` method to `AgentAgency` in `agentagency.py`
3. Instantiate and append the agent to `participants` in `agents.py`
4. Define the handoff signal the agent expects and emits in its system message

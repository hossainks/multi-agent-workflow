# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the workflow

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Run the multi-agent workflow
python agents.py
```

No test suite or linter is configured. Node.js (`npx`) must be available on PATH — it is used to launch all MCP servers at runtime.

## Environment variables

Copy `.env.example` (or create `.env`) with the following keys before running:

```
OPENAI_API_KEY=
MYSQL_HOST=
MYSQL_PORT=
MYSQL_USER=
MYSQL_PASS=
MYSQL_DB=
```

## Architecture

This is a **sequential multi-agent workflow** built on [AutoGen](https://github.com/microsoft/autogen) (`autogen_agentchat`, `autogen_ext`). Three agents run in a `RoundRobinGroupChat` and communicate by passing structured text in their chat messages. The loop terminates when any message contains `"REGISTRATION PROCESS COMPLETE"`.

```
agents.py          — entry point; instantiates model client, agents, team, and runs the task
agentagency.py     — AgentAgency factory: creates typed AssistantAgents with their MCP workbenches
mcpconfig.py       — McpConfig: static factory methods that return McpWorkbench instances for each tool
```

### Agent roles and handoff signals

| Agent | MCP workbenches | Handoff signal written |
|---|---|---|
| `DatabaseAgent` | MySQL | `DATABASE_DATA_READY → APIAgent should proceed next` |
| `ApiAgent` | REST API + Filesystem | `API_TESTING_COMPLETE → Excel Agent should …` |
| `ExcelAgent` | Excel | `REGISTRATION PROCESS COMPLETE` |

Agents coordinate purely through **message text** — there is no shared state object. Downstream agents must parse the upstream agent's message to extract data.

### MCP servers (launched via `npx` at runtime)

| Workbench | npm package | Purpose |
|---|---|---|
| MySQL | `@benborla29/mcp-server-mysql` | Query the registration DB |
| REST API | `dkmaker-mcp-rest-api` | Make HTTP calls (base URL configured in `mcpconfig.py`) |
| Filesystem | `@modelcontextprotocol/server-filesystem` | Read Postman JSON from `C:\Users\FXDCIU\Desktop\Claude-Test\Json-Files` |
| Excel | `@negokaz/excel-mcp-server` | Write results to `C:\Users\FXDCIU\Desktop\File-Test\devdata.xlsx` |

To add a new agent type: add a `get_*_workbench()` static method to `McpConfig`, then add a `create_*_agent()` method to `AgentAgency`, wire it in `agents.py`.

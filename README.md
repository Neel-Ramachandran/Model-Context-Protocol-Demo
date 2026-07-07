# MCP Demo Server

A minimal MCP (Model Context Protocol) server with 4 tools and a governance
layer. The idea: an AI agent can only call the tools it's allowed to. Before
any sensitive tool runs, the server checks the user's permissions.

## Setup

```
pip install -r requirements.txt
pip install uv
```

## Run with the Inspector

```
mcp dev server.py
```

Open the URL it prints, hit **Connect**, then go to the **Tools** tab. Don't
touch the Authentication section, it's not needed for a local server.

## The 4 tools

| Tool | Input | What it does |
|------|-------|-------------|
| `list_queues` | none | All queues with depth and status |
| `get_queue_depth` | queue_name | Depth for one queue |
| `search_logs` | keyword | Log lines matching a keyword |
| `restart_agent` | agent_id | **Blocked** by the permission check |

Try calling `restart_agent` in the Inspector. It returns a permission-denied
error, because that tool isn't in the current user's permission list. That's
the whole point of the governance layer.

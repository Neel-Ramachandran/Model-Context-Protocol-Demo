# MCP Demo Server

A small MCP (Model Context Protocol) server I built while learning how MCP
works. It has four tools with a permission layer on top. The thing I wanted to
show is that an AI agent shouldn't be able to call whatever it wants: before any
sensitive tool runs, the server checks whether the current user is actually
allowed to run it.

MCP is the protocol that lets an AI model call external tools in a structured
way. This server is a stripped-down example of that, plus the governance piece
that decides what's allowed.

## Setup

```
pip install -r requirements.txt
pip install uv
```

## Running it

```
mcp dev server.py
```

That launches the MCP Inspector. Open the URL it prints, click Connect, and go
to the Tools tab. You can ignore the Authentication section, it isn't needed for
running locally.

## The four tools

| Tool | Input | What it does |
|------|-------|--------------|
| `list_queues` | none | Lists all queues with depth and status |
| `get_queue_depth` | queue_name | Depth and status of one queue |
| `search_logs` | keyword | Log lines that match a keyword |
| `restart_agent` | agent_id | Blocked on purpose by the permission check |

The first three are read-only, so the user is allowed to run them.
`restart_agent` is the interesting one. It's a real action, and the current user
doesn't have permission for it, so trying to call it in the Inspector comes back
with a permission-denied error instead of doing anything.

## The point

`restart_agent` returns permission denied because it isn't in the user's
permission list:

```python
if "restart_agent" not in CURRENT_USER["permissions"]:
    return {"error": "Permission denied: restart_agent requires elevated access"}
```

That check is the whole reason the server exists. In a real system this is where
you'd stop an agent from doing something it shouldn't, and the user identity
would come from an actual auth layer instead of being hard-coded like it is here.

## Built with

- Python
- The MCP SDK (FastMCP)

## Author

Neel Ramachandran

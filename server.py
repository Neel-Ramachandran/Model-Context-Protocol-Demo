# ============================================================
#  server.py
#  A minimal MCP server with 4 tools and a governance layer.
#
#  The point of this demo: an AI agent can only call tools it is
#  allowed to call. Before any sensitive tool runs, the server
#  checks the current user's permissions. Read-only tools are
#  open; the one write/action tool (restart_agent) is blocked.
#
#  Run the Inspector:
#    pip install -r requirements.txt
#    pip install uv
#    mcp dev server.py
#  Then open the printed URL, hit Connect, and use the Tools tab.
# ============================================================

from mcp.server.fastmcp import FastMCP

# The MCP server. The name is what shows up in the Inspector.
mcp = FastMCP("mcp-demo")


# ------------------------------------------------------------
#  GOVERNANCE: who is calling, and what are they allowed to do.
#  In a real system this comes from a JWT / auth layer. Here it
#  is hard-coded so the permission check is easy to see.
# ------------------------------------------------------------
CURRENT_USER = {
    "user_id": "neel",
    "role": "intern",
    # note that "restart_agent" is deliberately NOT in this list
    "permissions": ["list_queues", "get_queue_depth", "search_logs"],
}


# ------------------------------------------------------------
#  Fake backend data so the tools have something to return.
#  Stands in for what would be real queue / log APIs.
# ------------------------------------------------------------
QUEUES = {
    "ORDERS.IN":    {"depth": 12, "status": "OK"},
    "PAYMENTS.IN":  {"depth": 3,  "status": "OK"},
    "SHIPPING.OUT": {"depth": 0,  "status": "IDLE"},
    "DLQ":          {"depth": 47, "status": "WARNING"},
}

LOGS = [
    "2026-05-27 09:14:02 INFO  ORDERS.IN consumer started",
    "2026-05-27 09:15:41 WARN  DLQ depth rising, now 47",
    "2026-05-27 09:16:10 ERROR PAYMENTS.IN timeout on connection reset",
    "2026-05-27 09:17:55 INFO  SHIPPING.OUT drained to 0",
]


# ------------------------------------------------------------
#  TOOLS
#  @mcp.tool() registers a function as a tool the AI can call.
#  The docstring is what the AI reads to decide when to use it,
#  so keep it clear. Every tool returns a dict.
# ------------------------------------------------------------

@mcp.tool()
def list_queues() -> dict:
    """List every queue with its current depth and status."""
    return {"queues": QUEUES}


@mcp.tool()
def get_queue_depth(queue_name: str) -> dict:
    """Return the current depth and status of one specific queue by name."""
    q = QUEUES.get(queue_name)
    if q is None:
        return {"error": f"No queue named {queue_name!r}"}
    return {"queue": queue_name, **q}


@mcp.tool()
def search_logs(keyword: str) -> dict:
    """Return all log lines that contain the given keyword (case-insensitive)."""
    kw = keyword.lower()
    hits = [line for line in LOGS if kw in line.lower()]
    return {"keyword": keyword, "matches": hits, "count": len(hits)}


@mcp.tool()
def restart_agent(agent_id: str) -> dict:
    """
    Restart a running agent by its ID. Requires elevated permissions.
    This is the governance demo: the AI can TRY to call this, but the
    permission check below stops it unless the user is allowed.
    """
    if "restart_agent" not in CURRENT_USER["permissions"]:
        return {"error": "Permission denied: restart_agent requires elevated access"}

    # If the user did have permission, the real restart call would go here.
    return {"status": "restarted", "agent_id": agent_id}


# ------------------------------------------------------------
#  ENTRY POINT
#  Only runs when executed directly (python server.py), not on import.
#  transport="stdio" is what the Inspector connects to.
# ------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")

"""
MCP - Model Context Protocol
==============================

MCP is an open standard by Anthropic that lets AI models connect to external tools and data.

Without MCP:
    User → Claude → (Claude guesses / hallucinates)

With MCP:
    User → Claude → MCP Client → MCP Server → Real API (Zomato, GitHub, DB...)
                                ↑
                        defined tools with schemas

Key concepts:
    - MCP Server : exposes tools (functions the AI can call)
    - MCP Client : connects Claude to the server
    - Tool       : a function with a name, description, and input schema
    - Tool Call  : Claude decides to call a tool based on user message
    - Tool Result: server runs the function, returns result to Claude

Flow:
    1. Client sends user message + list of available tools to Claude
    2. Claude reads tools, decides which to call
    3. Client executes the tool on the server
    4. Result sent back to Claude
    5. Claude forms final response

Real MCP Servers that exist today:
    - GitHub MCP     : search repos, create issues, read files
    - Postgres MCP   : query databases
    - Brave Search   : web search
    - Slack MCP      : send messages, read channels
    - Filesystem MCP : read/write local files

Zomato MCP (what we're building):
    - search_restaurants(city, cuisine)
    - get_menu(restaurant_id)
    - add_to_cart(item_id, quantity)
    - place_order(cart_id, address)
    - track_order(order_id)

Requires: Python 3.10+, pip install mcp anthropic
"""

print("MCP = giving Claude hands to interact with real systems")
print("Tools are like API endpoints that Claude can decide to call")

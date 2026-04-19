"""
Zomato MCP Client — Working Demo (Python 3.9 compatible)
=========================================================
Uses Anthropic tool calling directly (same mechanism MCP uses under the hood).
When MCP SDK supports Python 3.9, swap the tool definitions for an MCP connection.

Run: python3 03_zomato_client.py
Requires: pip install anthropic, ANTHROPIC_API_KEY in .env
"""

import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

import anthropic

# Import actual tool implementations from server
from zomato_mcp_server_tools import search_restaurants, get_menu, add_to_cart, place_order, track_order

client = anthropic.Anthropic()

# ── Tool Definitions (same schema MCP server would expose) ────────────────────

TOOLS = [
    {
        "name": "search_restaurants",
        "description": "Search restaurants by city and cuisine",
        "input_schema": {
            "type": "object",
            "properties": {
                "city":    {"type": "string", "description": "City name"},
                "cuisine": {"type": "string", "description": "Cuisine type (optional)"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_menu",
        "description": "Get the menu for a restaurant by its ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "string"}
            },
            "required": ["restaurant_id"]
        }
    },
    {
        "name": "add_to_cart",
        "description": "Add a menu item to the cart",
        "input_schema": {
            "type": "object",
            "properties": {
                "item_id":  {"type": "string"},
                "quantity": {"type": "integer"}
            },
            "required": ["item_id", "quantity"]
        }
    },
    {
        "name": "place_order",
        "description": "Place the order with a delivery address",
        "input_schema": {
            "type": "object",
            "properties": {
                "address": {"type": "string"}
            },
            "required": ["address"]
        }
    },
    {
        "name": "track_order",
        "description": "Track status of an existing order",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    },
]

# ── Tool Executor ──────────────────────────────────────────────────────────────

def execute_tool(name: str, inputs: dict) -> str:
    print(f"\n  [tool] {name}({inputs})")
    if name == "search_restaurants": result = search_restaurants(**inputs)
    elif name == "get_menu":         result = get_menu(**inputs)
    elif name == "add_to_cart":      result = add_to_cart(**inputs)
    elif name == "place_order":      result = place_order(**inputs)
    elif name == "track_order":      result = track_order(**inputs)
    else:                            result = {"error": f"Unknown tool: {name}"}
    print(f"  [result] {result}")
    return json.dumps(result)

# ── Agent Loop ─────────────────────────────────────────────────────────────────

def run_agent(user_message: str):
    print(f"\nUser: {user_message}")
    print("-" * 50)

    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )

        # Claude wants to call a tool
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user",      "content": tool_results})

        # Claude has a final answer
        else:
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\nClaude: {block.text}")
            break

# ── Test ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_agent("Order 2 Chicken Biryanis from an Indian restaurant in Mumbai to 42 Linking Road")

"""
Zomato MCP Server
==================
Exposes food ordering tools that Claude can call via MCP protocol.

Run this server:  python3 02_zomato_mcp_server.py
Requires: Python 3.10+, pip install mcp
"""

# from mcp.server import Server           # needs Python 3.10+
# from mcp.server.stdio import stdio_server
# import mcp.types as types

# ── Mock Zomato Data ──────────────────────────────────────────────────────────

RESTAURANTS = {
    "r1": {"name": "Biryani Blues",   "cuisine": "Indian", "rating": 4.5, "city": "Mumbai"},
    "r2": {"name": "Pizza Palace",    "cuisine": "Italian","rating": 4.2, "city": "Mumbai"},
    "r3": {"name": "Dragon Wok",      "cuisine": "Chinese","rating": 4.0, "city": "Mumbai"},
}

MENUS = {
    "r1": [
        {"id": "m1", "name": "Chicken Biryani", "price": 280},
        {"id": "m2", "name": "Mutton Biryani",  "price": 350},
        {"id": "m3", "name": "Raita",           "price": 50},
    ],
    "r2": [
        {"id": "m4", "name": "Margherita Pizza","price": 320},
        {"id": "m5", "name": "Pasta Arrabiata", "price": 240},
    ],
}

cart = {}

# ── Tool Implementations ───────────────────────────────────────────────────────

def search_restaurants(city: str, cuisine: str = None) -> list:
    results = [r for r in RESTAURANTS.values() if r["city"].lower() == city.lower()]
    if cuisine:
        results = [r for r in results if r["cuisine"].lower() == cuisine.lower()]
    return results

def get_menu(restaurant_id: str) -> list:
    return MENUS.get(restaurant_id, [])

def add_to_cart(item_id: str, quantity: int) -> dict:
    cart[item_id] = cart.get(item_id, 0) + quantity
    return {"cart": cart, "message": f"Added {quantity}x {item_id} to cart"}

def place_order(address: str) -> dict:
    if not cart:
        return {"error": "Cart is empty"}
    total = sum(
        next((item["price"] for menu in MENUS.values() for item in menu if item["id"] == item_id), 0) * qty
        for item_id, qty in cart.items()
    )
    order_id = "ORD" + str(hash(address))[-6:]
    return {"order_id": order_id, "total": total, "address": address, "status": "confirmed"}

def track_order(order_id: str) -> dict:
    return {"order_id": order_id, "status": "Out for delivery", "eta": "25 mins"}

# ── MCP Server Setup (Python 3.10+) ───────────────────────────────────────────
#
# app = Server("zomato-mcp")
#
# @app.list_tools()
# async def list_tools():
#     return [
#         types.Tool(name="search_restaurants",
#                    description="Search restaurants by city and cuisine",
#                    inputSchema={"type":"object","properties":{
#                        "city":{"type":"string"},
#                        "cuisine":{"type":"string"}
#                    },"required":["city"]}),
#
#         types.Tool(name="get_menu",
#                    description="Get menu for a restaurant",
#                    inputSchema={"type":"object","properties":{
#                        "restaurant_id":{"type":"string"}
#                    },"required":["restaurant_id"]}),
#
#         types.Tool(name="add_to_cart",
#                    description="Add an item to cart",
#                    inputSchema={"type":"object","properties":{
#                        "item_id":{"type":"string"},
#                        "quantity":{"type":"integer"}
#                    },"required":["item_id","quantity"]}),
#
#         types.Tool(name="place_order",
#                    description="Place the order",
#                    inputSchema={"type":"object","properties":{
#                        "address":{"type":"string"}
#                    },"required":["address"]}),
#
#         types.Tool(name="track_order",
#                    description="Track an existing order",
#                    inputSchema={"type":"object","properties":{
#                        "order_id":{"type":"string"}
#                    },"required":["order_id"]}),
#     ]
#
# @app.call_tool()
# async def call_tool(name: str, arguments: dict):
#     if name == "search_restaurants": return search_restaurants(**arguments)
#     if name == "get_menu":           return get_menu(**arguments)
#     if name == "add_to_cart":        return add_to_cart(**arguments)
#     if name == "place_order":        return place_order(**arguments)
#     if name == "track_order":        return track_order(**arguments)
#
# if __name__ == "__main__":
#     import asyncio
#     async def main():
#         async with stdio_server() as (read, write):
#             await app.run(read, write, app.create_initialization_options())
#     asyncio.run(main())

# ── Quick sanity test without MCP ─────────────────────────────────────────────
if __name__ == "__main__":
    print(search_restaurants("Mumbai", "Indian"))
    print(get_menu("r1"))
    print(add_to_cart("m1", 2))
    print(place_order("123 MG Road, Mumbai"))

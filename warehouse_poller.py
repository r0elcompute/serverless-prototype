"""
[DEPRECATED - THE MERIDIAN PIVOT]
This 5-minute polling mechanism has been killed by client mandate (Solstice Events Co.).
Replaced by event-driven serverless webhook listener (see serverless_handler.py).
"""

import time
import json
from datetime import datetime

# Simulated local cache file
CACHE_FILE = "inventory_cache.json"

def fetch_warehouse_api():
    """Simulates polling an external warehouse API for inventory levels."""
    # In a real app, this would be a requests.get('https://api.warehouse.com/stock')
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Polling warehouse API...")
    
    # Mock stock data response
    mock_stock_data = {
        "SKU-98765": {"item": "Wireless Mouse", "stock_qty": 45, "status": "In Stock"},
        "SKU-12345": {"item": "Mechanical Keyboard", "stock_qty": 0, "status": "Out of Stock"},
        "SKU-54321": {"item": "USB-C Hub", "stock_qty": 12, "status": "In Stock"}
    }
    return mock_stock_data

def update_local_cache(data):
    """Caches the fetched stock data locally."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("[INFO] Local cache successfully updated.")
    except Exception as e:
        print(f"[ERROR] Failed to update cache: {e}")

def query_inventory(sku):
    """Exposes a query function for the support tool to check stock status."""
    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
            
        item = cache.get(sku)
        if item:
            return {"status": 200, "sku": sku, "details": item}
        else:
            return {"status": 404, "error": "SKU not found in local cache"}
    except FileNotFoundError:
        return {"status": 500, "error": "Cache not initialized. Run poller first."}

if __name__ == "__main__":
    print("--- Day 3: Original Polling & Caching Service ---")
    
    # Initial poll & cache generation
    current_stock = fetch_warehouse_api()
    update_local_cache(current_stock)
    
    # Test the query endpoint behavior
    print("\n[TEST] Querying support tool endpoint for SKU-98765...")
    result = query_inventory("SKU-98765")
    print("Query Result:", json.dumps(result, indent=2))
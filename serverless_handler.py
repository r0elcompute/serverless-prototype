import json

def handle_serverless_event(event: dict) -> dict:
    """
    Simulates a serverless function execution.
    It receives an event payload (like an incoming webhook) and processes it on-demand.
    """
    print("[INFO] Serverless compute instance spun up instantly.")
    
    # Extract data from the incoming event
    payload = event.get("body", {})
    item_id = payload.get("item_id", "UNKNOWN_ITEM")
    action = payload.get("action", "CHECK_STOCK")
    
    if action == "CHECK_STOCK":
        response_data = {
            "status": "success",
            "message": f"Serverless function successfully processed stock check for item: {item_id}",
            "compute_model": "serverless"
        }
    else:
        response_data = {
            "status": "error",
            "message": "Unsupported action payload."
        }
        
    return {
        "statusCode": 200,
        "body": json.dumps(response_data)
    }
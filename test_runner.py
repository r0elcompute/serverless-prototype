from serverless_handler import handle_serverless_event

if __name__ == "__main__":
    # Simulate an incoming webhook payload triggered by an external service
    mock_event = {
        "body": {
            "item_id": "SKU-98765",
            "action": "CHECK_STOCK"
        }
    }
    
    print("--- Invoking Serverless Function Locally ---")
    result = handle_serverless_event(mock_event)
    print("Execution Result:", result)
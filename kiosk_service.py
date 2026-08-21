import json
from datetime import datetime

# In-memory database simulation for attendee check-in states
ATTENDEE_DB = {
    "ATTENDEE-001": {"name": "Alice Wang", "status": "Registered", "badge_printed": False},
    "ATTENDEE-002": {"name": "Bob Smith", "status": "Registered", "badge_printed": False},
}

def simulate_qr_scan(attendee_id):
    """
    Simulates scanning an attendee's QR code at the kiosk.
    Under the new async pivot model, this does NOT wait for the printer. 
    It publishes a request and sets status to 'Pending'.
    """
    print(f"\n[SCAN] QR Code scanned for: {attendee_id}")
    
    attendee = ATTENDEE_DB.get(attendee_id)
    if not attendee:
        return {"status": 404, "message": "Attendee not found in system."}
    
    # Check for duplicate-scan protection
    if attendee["badge_printed"] or attendee["status"] == "Checked In":
        print(f"[BLOCKED] Duplicate scan detected for {attendee_id}. No second badge will be printed.")
        return {
            "status": 400, 
            "message": f"Duplicate scan: {attendee['name']} is already checked in."
        }
    
    # Asynchronous handoff: Mark as pending print
    attendee["status"] = "Pending Print"
    print(f"[INFO] Print request queued asynchronously for {attendee['name']}. UI state: PENDING.")
    
    return {
        "status": 202,
        "message": f"Print request accepted for {attendee['name']}. Awaiting webhook confirmation.",
        "attendee_state": attendee["status"]
    }

def handle_printer_webhook_callback(payload):
    """
    The new webhook endpoint called asynchronously by the badge printer vendor 
    once the physical print job is successfully completed.
    """
    attendee_id = payload.get("attendee_id")
    print(f"\n[WEBHOOK RECEIVED] Callback from printer vendor for: {attendee_id}")
    
    attendee = ATTENDEE_DB.get(attendee_id)
    if not attendee:
        return {"statusCode": 404, "body": "Attendee record missing."}
    
    # Update state upon successful callback confirmation
    if payload.get("print_success") is True:
        attendee["badge_printed"] = True
        attendee["status"] = "Checked In"
        print(f"[SUCCESS] Badge printed successfully! UI updated to 'CHECKED IN' for {attendee['name']}.")
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success", "attendee": attendee_id, "final_state": "Checked In"})
        }
    else:
        print("[ERROR] Print job failed at the hardware level.")
        return {"statusCode": 500, "body": json.dumps({"status": "error", "message": "Print failed"})}

if __name__ == "__main__":
    print("--- Solstice Events Co. Asynchronous Kiosk Pivot Simulation ---")
    
    # 1. First scan for Alice (Triggers async queue)
    scan_result_1 = simulate_qr_scan("ATTENDEE-001")
    print("Scan 1 Response:", json.dumps(scan_result_1, indent=2))
    
    # 2. Simulate duplicate scan immediately before webhook arrives (Should be blocked)
    duplicate_result = simulate_qr_scan("ATTENDEE-001")
    print("Duplicate Scan Response:", json.dumps(duplicate_result, indent=2))
    
    # 3. Simulate the webhook callback arriving from the printer vendor
    webhook_payload = {"attendee_id": "ATTENDEE-001", "print_success": True}
    webhook_response = handle_printer_webhook_callback(webhook_payload)
    print("Webhook Response:", webhook_response)
    
    # 4. Try scanning Alice a third time AFTER successful check-in (Should still be blocked by duplicate guard)
    post_checkin_scan = simulate_qr_scan("ATTENDEE-001")
    print("Post-Checkin Scan Response:", json.dumps(post_checkin_scan, indent=2))
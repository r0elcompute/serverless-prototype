import json
from datetime import datetime

# In-memory database simulation scaled to 3+ test attendees as requested by Solstice Events Co.
ATTENDEE_DB = {
    "ATTENDEE-001": {"name": "Alice Wang", "status": "Registered", "badge_printed": False},
    "ATTENDEE-002": {"name": "Bob Smith", "status": "Registered", "badge_printed": False},
    "ATTENDEE-003": {"name": "Charlie Kariuki", "status": "Registered", "badge_printed": False}
}

def simulate_qr_scan(attendee_id):
    """
    Simulates scanning an attendee's QR code at the kiosk.
    Publishes an async request and sets status to 'Pending' (No longer blocking).
    """
    print(f"\n[SCAN] QR Code scanned for: {attendee_id}")
    
    attendee = ATTENDEE_DB.get(attendee_id)
    if not attendee:
        return {"status": 404, "message": "Attendee not found in system."}
    
    # Duplicate-scan protection rule
    if attendee["badge_printed"] or attendee["status"] in ["Checked In", "Pending Print"]:
        print(f"[BLOCKED] Duplicate scan detected for {attendee['name']} ({attendee_id}). Second badge suppressed.")
        return {
            "status": 400, 
            "message": f"Duplicate scan: {attendee['name']} is already processed/checked in."
        }
    
    # Asynchronous handoff
    attendee["status"] = "Pending Print"
    print(f"[INFO] Print request queued for {attendee['name']}. UI state: PENDING.")
    
    return {
        "status": 202,
        "message": f"Print request accepted for {attendee['name']}. Awaiting webhook confirmation.",
        "attendee_state": attendee["status"]
    }

def handle_printer_webhook_callback(payload):
    """
    Webhook endpoint receiving asynchronous callbacks from the badge printer vendor.
    """
    attendee_id = payload.get("attendee_id")
    print(f"\n[WEBHOOK RECEIVED] Callback from vendor for: {attendee_id}")
    
    attendee = ATTENDEE_DB.get(attendee_id)
    if not attendee:
        return {"statusCode": 404, "body": "Attendee record missing."}
    
    if payload.get("print_success") is True:
        attendee["badge_printed"] = True
        attendee["status"] = "Checked In"
        print(f"[SUCCESS] Badge printed! UI updated to 'CHECKED IN' for {attendee['name']}.")
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success", "attendee": attendee_id, "final_state": "Checked In"})
        }
    else:
        print("[ERROR] Print job failed at hardware level.")
        return {"statusCode": 500, "body": json.dumps({"status": "error", "message": "Print failed"})}

if __name__ == "__main__":
    print("--- Solstice Events Co. Asynchronous Kiosk Pivot (3+ Attendees & Duplicate Test) ---")
    
    # 1. Scan Attendee 001 (Alice) -> Enters Pending
    simulate_qr_scan("ATTENDEE-001")
    
    # 2. Test Duplicate-Scan Case on Alice BEFORE her webhook arrives (Out-of-order simulation)
    print("\n[TEST CASE] Attempting duplicate scan on Alice while print is pending...")
    simulate_qr_scan("ATTENDEE-001")
    
    # 3. Scan Attendee 002 (Bob) -> Enters Pending
    simulate_qr_scan("ATTENDEE-002")
    
    # 4. Scan Attendee 003 (Charlie) -> Enters Pending
    simulate_qr_scan("ATTENDEE-003")
    
    # 5. Receive Webhook confirmations for Alice and Bob
    handle_printer_webhook_callback({"attendee_id": "ATTENDEE-001", "print_success": True})
    handle_printer_webhook_callback({"attendee_id": "ATTENDEE-002", "print_success": True})
    
    # 6. Post-Checkin Duplicate Test: Try scanning Alice again AFTER she is fully checked in
    print("\n[TEST CASE] Attempting duplicate scan on Alice AFTER successful check-in...")
    simulate_qr_scan("ATTENDEE-001")
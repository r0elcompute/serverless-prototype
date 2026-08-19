# Blocker Journal - Serverless Topic

## 1. Resources Consulted
* *The Open-Source Serverless Guide* (Community architecture patterns & event-driven models)
* *TutorialsPoint: Serverless Computing Definition, Application, Advantages*
* Python standard library documentation (`json` module parsing and dictionary handling)

## 2. Hour-by-Hour Troubleshooting Log & Dead Ends
* **[Day 1 - 09:00]** *Concept Definition:* Researched how serverless fits into event-driven webhook architectures versus traditional polling loops. Decided to build a standalone, lightweight local simulation to avoid heavy cloud IAM/billing setups while meeting functional requirements.
* **[Day 1 - 11:30]** *Implementation Hurdle:* Initially considered AWS Lambda with complex zip packaging. Hit potential local emulation friction. *Resolution:* Shifted to a pure function handler pattern (`serverless_handler.py`) paired with an execution harness (`test_runner.py`) to keep code modular and transparent.
* **[Day 2 - 14:00]** *Payload Parsing Test:* Encountered strict JSON formatting constraints when passing mock HTTP event structures. *Resolution:* Implemented safe dictionary `.get()` lookups with default fallbacks to ensure graceful failure on malformed webhook payloads.

## 3. Final Working State Verification
* Successfully executed `python test_runner.py`.
* Verified that the serverless function spins up on demand, parses incoming event items, and returns a structured `200 OK` JSON response simulating a webhook trigger.
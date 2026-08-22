# Serverless Webhook Event Handler Prototype

A lightweight, local-first serverless function prototype.

## Overview
This project simulates an event-driven serverless compute model. Instead of relying on a persistent server or heavy cloud infrastructure (like paid AWS accounts), it demonstrates how application logic can be structured as an isolated handler that spins up on demand to process incoming event payloads (such as webhook triggers).

## Project Structure
* `serverless_handler.py`: Contains the core serverless function logic (`handle_serverless_event`) that parses incoming event data and returns a structured JSON response.
* `test_runner.py`: A local execution harness used to invoke the serverless function and verify its output without requiring a cloud deployment.
* `BLOCKER_JOURNAL.md`: Documents the self-guided learning process, resources consulted, troubleshooting steps, and error logs.

## How to Run Locally
1. Ensure you have Python installed.
2. Clone the repository
3. Run the test runner script to simulate an incoming webhook trigger:
   ```bash
   python test_runner.py

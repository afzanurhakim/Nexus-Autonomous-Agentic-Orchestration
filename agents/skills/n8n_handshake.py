import os
import requests
from loguru import logger
from dotenv import load_dotenv

# Load security environment
load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
N8N_AUTH_TOKEN = os.getenv("N8N_AUTH_TOKEN")

def trigger_n8n_sync(task_data):
    """
    The 'Nerve Center' Skill. 
    Transmits AI-reasoned JSON payloads to the n8n orchestration layer.
    """
    
    # 1. Validation: Ensure we aren't sending empty noise
    if not task_data:
        logger.error("⚠️ Handshake aborted: No task data provided.")
        return {"status": "error", "message": "Empty payload"}

    # 2. Security: Header-based Authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {N8N_AUTH_TOKEN}",
        "X-Nexus-Agent": "Alpha-1.0"
    }

    logger.info(f"🔗 Initiating Handshake with n8n for task: {task_data.get('title', 'System Sync')}")

    try:
        # 3. Execution: The Outbound POST request
        # We use a 10s timeout to prevent the 'Brain' from hanging
        response = requests.post(
            N8N_WEBHOOK_URL, 
            json=task_data, 
            headers=headers, 
            timeout=10
        )

        # 4. Error Handling: Checking the 'HTTP Heartbeat'
        response.raise_for_status() 
        
        logger.success("✅ Handshake Successful: Payload delivered to Orchestrator.")
        return response.json()

    except requests.exceptions.Timeout:
        logger.error("❌ Handshake Timeout: n8n server took too long to respond.")
        return {"status": "error", "message": "Connection Timeout"}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Handshake Critical Failure: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test script for local debugging
    test_payload = {"title": "Test Handshake", "priority": "Low", "action": "test"}
    print(trigger_n8n_sync(test_payload))
import os
import time
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

# Import custom skills
from agents.skills.n8n_handshake import trigger_n8n_sync
from agents.skills.deduplication import check_duplicate_task

# 1. Load Environment & Security
load_dotenv()
N8N_URL = os.getenv("N8N_WEBHOOK_URL")
AGENT_MODE = os.getenv("AGENT_MODE", "production")

logger.info(f"Nexus Starting in {AGENT_MODE} mode...")

# 2. The 'Heartbeat' Routine (from HEARTBEAT.md)
def heartbeat_routine():
    logger.info("Heartbeat: Scanning Monday.com for stalled tasks...")
    
    # Logic: Call n8n to check for 'Stalled' status
    # This is where the 'Pulse' actually happens
    payload = {"action": "check_stalls", "timestamp": time.time()}
    try:
        response = trigger_n8n_sync(payload)
        logger.success(f"✅ Heartbeat Sync Complete: {response.get('status', 'OK')}")
    except Exception as e:
        logger.error(f"❌ Heartbeat Failure: {str(e)}")

# 3. The 'Meeting Processor' (The Reasoning Layer)
def process_new_meeting(transcript):
    logger.info("Soul: Reasoning through meeting transcript...")
    
    # Here you would call your LLM (OpenAI/Gemini) 
    # using the constraints in your SOUL.md
    
    # Placeholder for the Agent's Decision
    suggested_task = {"title": "Update Brand Deck", "priority": "High"}
    
    # Perform the 'Deduplication' Check
    if not check_duplicate_task(suggested_task):
        trigger_n8n_sync(suggested_task)
        logger.success("🎯 Task Created: No duplicates found.")
    else:
        logger.warning("⚠️ Task Skipped: Duplicate detected via Cosine Similarity.")

# 4. Initialize the Scheduler (The Temporal Daemon)
scheduler = BackgroundScheduler()
scheduler.add_job(heartbeat_routine, 'interval', minutes=15)

if __name__ == "__main__":
    scheduler.start()
    logger.info("Persistent Loop Active. Press Ctrl+C to exit.")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Nexus Shutdown Safely.")

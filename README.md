# Nexus-Alpha: Autonomous Agentic Orchestration

Nexus-Alpha is a **Stateful, Proactive Agentic System** designed to bridge the "Execution Gap" in creative production environments. Unlike standard linear automations, Nexus-Alpha utilizes a **"Brain-and-Muscles"** architecture—combining high-level LLM reasoning with a robust n8n orchestration layer.

---

## System Architecture



The system is built on four core pillars:

1. **The Mind (`agents/SOUL.md`):** Defines the agent's identity, Bithour-specific SOPs, and "Creative Producer" persona.
2. **The Pulse (`agents/HEARTBEAT.md`):** A persistent 15-minute temporal daemon that proactively scans for stalled tasks on Monday.com.
3. **The Nerves (`agents/skills/`):** Custom Python logic for **Semantic Deduplication** and secure n8n handshakes.
4. **The Muscles (`workflows/`):** Production-ready n8n blueprints for API execution across **Monday.com** and **Notion**.

Flowchart:

 ```mermaid
   graph TD
  %% Input Triggers
    A1[Meeting Transcript] --> B[main.py Kernel]
    A2[HEARTBEAT.md Trigger] -- "Interval: 15 Mins" --> B
    
    %% The Unified Brain
    B --> C{SOUL.md Reasoning}
    C --> D[Deduplication Skill]
    D --> E[n8n_handshake.py]
    
    %% Execution Layer
    E --> F[n8n Orchestrator]
    F --> G[Monday.com Task Sync]
    F --> I[Notion Dashboard]
  ```  

---

## Key Features

### 1. Industrial-Grade Reliability
* **Fault Tolerance:** Built-in exponential backoff and error logging for API stability.
* **Semantic Integrity:** Uses vector-based deduplication to prevent task clutter.
  * *Logic:* $\text{similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$
* **Human-in-the-Loop (HITL):** Critical actions (budget changes/deletions) require a manual "handshake" via Slack.

### 2. Business Intelligence & ROI
* **Real-Time Telemetry:** Every execution logs token expenditure (USD) to a **Notion Executive Dashboard**.
* **Efficiency Mapping:** Tracks "Human Hours Saved" to provide a transparent ROI for the agency.

### 3. Data Sovereignty & Security
* **Zero-Leak Policy:** Credentials managed via `.env` (strictly ignored by Git).
* **Edge Deployment:** Designed for local VPS or Mac Mini hosting to keep internal Bithour meeting data private.

---

## Repository Structure

```text
NexusMeeting-AI/
├── agents/
│   ├── SOUL.md                 # Agent Identity & Persona
│   ├── HEARTBEAT.md            # Temporal Logic & Routines
│   └── skills/
│       ├── n8n_handshake.py    # API Transmission Skill
│       └── deduplication.py    # Semantic Similarity Filter
├── workflows/
│   ├── nexus_core.json         # n8n Core Orchestrator
│   └── roi_dashboard.json      # Notion ROI Telemetry
├── main.py                     # System Kernel & Scheduler
├── .env.example                # Configuration Template
├── .gitignore                  # Security Guardrails
├── requirements.txt            # Dependency List
└── README.md                   # System Documentation
```

---

**Getting Started**

**Prerequisites**
- Python 3.10+
- n8n (Local or Cloud instance)
- API Keys: Gemini/OpenAI, Monday.com, Notion.

**Installation**
1. **Clone the repository**
```bash
git clone https://github.com/afzanurhakim/NexusMeeting-AI.git
cd NexusMeeting-AI
```
2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Configure Security**
```bash
cp .env.example .env
# Update .env with your specific API credentials
```

**Deployment**
1. Import the .json files from /workflows into your n8n instance.

2. Start the persistent agent loop:
```bash
python main.py
```

---





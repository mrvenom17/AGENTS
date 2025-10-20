# ⚙️ OP Shell — Intent-Driven Secure Shell Automation

**“Precision before power.”**

OP Shell is an intelligent command execution framework that turns **human intent into safe, deterministic shell actions**.  
It bridges the gap between natural language and system control — built for **DevOps, Red/Blue Teamers, and SysAdmins** who demand speed *without ever sacrificing security or auditability.*

---

## 🧭 Vision

> Eliminate the cognitive and operational risk in shell environments  
> by creating a trusted, auditable, and adaptive automation layer  
> that understands what you mean — and executes only what is safe.

---

## 🧩 Core Principles

1. **Determinism > Guesswork** — Every intent is mapped via explicit rules.  
2. **Safety > Speed** — Nothing runs until verified, sandboxed, and logged.  
3. **Transparency > Trust** — Every action leaves a trail you can audit.  
4. **Extensibility > Lock-in** — Modular by design; add new intents, parsers, or agents without breaking core logic.

---

## 🚀 What It Does

| Feature | Description |
|----------|-------------|
| 🔍 **Intent Parsing** | Converts high-level user requests into precise command templates. |
| 🧠 **Rule Engine** | Deterministic YAML/JSON mappings for predictable behavior. |
| 🧱 **Sandbox Execution** | Runs every command inside ephemeral Docker/Podman containers. |
| 🛡️ **RBAC & Deny-List** | Prevents unauthorized or destructive operations (`rm`, `sudo`, etc.). |
| 🧾 **Dry-Run Mode** | Simulates execution to show exactly what would happen. |
| 📜 **Audit Logging** | Stores timestamp, user, intent, command, and output hash. |
| 🌐 **UI/CLI Interface** | Minimal web dashboard or command-line client for interaction. |

---

## 🧠 Architectural Overview

User → [Intent Parser] → [Rule Engine] → [Policy Validator]
→ [Sandbox Executor] → [Audit Logger] → [UI/Dashboard]


Each layer is **independent, replaceable, and testable** — built for zero-trust environments.

---

## 🔩 Tech Stack

| Layer | Tool / Framework |
|-------|------------------|
| Backend | Python 3 + FastAPI |
| Rule Engine | Custom YAML/JSON parser |
| Sandbox | Docker / Podman (ephemeral containers) |
| Database | SQLite (MVP) → PostgreSQL (production) |
| Frontend | React + Tailwind / FastAPI HTML (CLI optional) |
| Auth | JWT / API Key |
| CI/CD | GitHub Actions |
| Infra | Local / VPS / Vercel deployment |

---

## 🧱 Folder Structure

op-shell/
├── api/
│ ├── main.py # FastAPI entrypoint
│ ├── routes/ # Intent, sandbox, logs endpoints
│ └── auth/ # JWT / API key middleware
├── core/
│ ├── rule_engine.py # Intent → Command mapping
│ ├── sandbox_manager.py # Docker container executor
│ ├── policy_validator.py# RBAC / deny-list enforcement
│ └── logger.py # Audit logger
├── config/
│ ├── intents.yaml # Intent-command mappings
│ ├── rbac.json # User roles & permissions
│ └── settings.py
├── ui/
│ ├── dashboard/ # React frontend (optional)
│ └── cli.py # Minimal CLI interface
├── tests/
│ └── test_rules.py # Unit tests for mappings
└── README.md


---

## ⚙️ Getting Started

### 1️⃣ Prerequisites
- Python 3.10+  
- Docker or Podman  
- Node (only if you’re running the React dashboard)

### 2️⃣ Setup

```bash
# Clone the repo
git clone https://github.com/yourname/op-shell.git
cd op-shell

# Create virtual environment
python -m venv venv && source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

#Run Sandbox Service
docker build -t op-shell-sandbox .
docker run --rm -it op-shell-sandbox

#Launch API
uvicorn api.main:app --reload

#Test an Intent
curl -X POST http://localhost:8000/intent \
     -H "Content-Type: application/json" \
     -d '{"user":"dev","intent":"list all files"}'
```
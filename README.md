# Upsum — Project Nexus

> *A sovereign Swedish knowledge platform designed to replace generic encyclopedias with a fast, fact‑centric experience built for Swedish language and intent.*


## 🜲 Overview

## 🚀 Getting Started

### Quick Start (Windows)

To install dependencies and launch both backend and frontend automatically, run:

```
RUNME.bat
```

This will:
- Set up Python virtual environment and install backend dependencies
- Install frontend dependencies (npm)
- Start backend (http://localhost:8000) and frontend (http://localhost:5173) in new terminals

If you encounter permission issues, right-click and run as administrator or check your Python/npm installation.

### Frontend (React + Vite)

1. Open a terminal in `frontend/`
2. Install dependencies:
  ```sh
  npm install
  ```
3. Start the development server:
  ```sh
  npm run dev
  ```
4. Open [http://localhost:5173](http://localhost:5173) to view the app.

### Backend (FastAPI)

1. Open a terminal in `backend/`
2. Create a virtual environment (optional but recommended):
  ```sh
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```
3. Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
4. Start the backend server:
  ```sh
  uvicorn main:app --reload
  ```
5. The API will be available at [http://localhost:8000](http://localhost:8000)

---

## 🏗️ Project Structure

```
Upsum/
├── backend/    # FastAPI backend (Python)
├── frontend/   # React frontend (Vite)
├── data/       # Data sources, Wikipedia dumps, etc.
├── docs/       # Documentation, diagrams
└── README.md   # Project overview and setup
```

---

**Codename:** Nexus  
**Project name:** Upsum  

Upsum is the next generation of Swedish knowledge — an independent and privacy‑minded platform built around the idea of *Swedish linguistic sovereignty*.  
It combines the reliability of Wikipedia’s factual backbone with a modern, Nordic‑themed design and a clean, dark-native interface.

The goal: to create **the next Wikipedia for Sweden**, purpose-built for Swedish readers, dialects, and expressions.

---

## 🌐 What is Project Nexus?

### Swedish‑First
Upsum treats Swedish as a first‑class citizen. Its knowledge model is tuned to understand Swedish grammar, nuance, and dialects — including compound words, regional phrasing, and idiomatic structures.

### Fact‑Centric
Every topic and claim is backed by traceable, verifiable sources. Upsum emphasizes accuracy and transparency — *no distractions, no bias, no noise.*

### Privacy‑Focused
Your curiosity should never come at the cost of your privacy.  
No ads, no tracking, no profiling — just **pure knowledge** at incredible speed.

---

## 🕯️ Why It Matters

### Language Sovereignty
- Swedish nuance is interpreted correctly.  
- Dialect and colloquial input are recognized.  
- Compounds and definiteness are resolved naturally.

### Trustworthy by Design
- Citation‑first presentation of facts.  
- Transparent provenance for all data.  
- Ad‑free reading, no interruptions.

### Built for Speed
- Extremely lightweight interface.  
- Fast caching for trending topics.  
- Stable performance even at scale.

---

## ⚙️ How It Works

### Natural Swedish Input
Upsum’s parser understands:
- Complex compounds and declension patterns.  
- Automatic normalization of definiteness and context.  
- Mapping of informal phrasing to formal semantic intent.

### Sovereign Data Layer
- Real‑time synchronization with Swedish Wikipedia content.  
- Planned integrations with official Swedish data sources:  
  *SCB, Bolagsverket, Lantmäteriet, Språkbanken.*  
- Transparent citations displayed alongside every claim.

### Oscyra Design System
- Minimalist, Nordic-inspired interface.  
- **Dark-first UX** — no light mode.  
- Built for clarity, speed, and calm visual focus.  
- Inspired by the Klar design language.

---

## 🛠️ Technology & Architecture (Conceptual)

- **Core**: Python & Go backend (API orchestration + data normalization).  
- **Frontend**: Lightweight Next.js or custom framework.  
- **Data**: Wikipedia dumps, structured Swedish datasets.  
- **Cache Layer**: Optimized object storage + edge caching.  
- **Privacy**: Zero analytics, optional local caching.  

---

## 🔮 Roadmap

| Phase | Goal | Status |
|-------|------|--------|
| Alpha | Core Wikipedia ingestion + Swedish NLP | 🟡 In Progress |
| Beta  | Interface with Oscyra design system | ⚪ Planned |
| 1.0   | Public release with sovereign data & full backend | ⚪ Planned |

---

## 🧭 Vision

Upsum’s mission is **to give Sweden back its knowledge — in its own language, on its own terms.**  
By merging verified information with linguistic precision, Upsum becomes more than an encyclopedia.  
It becomes **a national knowledge core**, sovereign, neutral, and enduring.

---

## 🧩 License and Attribution

- Built upon open data contributions from [Wikipedia](https://www.wikipedia.org) under the Creative Commons Attribution‑ShareAlike License.  
- Planned integrations with public datasets under compatible open licenses.

---

## 🌒 Design Reference

> “Form follows clarity.”  
> — Oscyra Design Philosophy

Dark, minimal, and purely functional — Upsum reflects Swedish calm.  
Every pixel serves comprehension, never distraction.

---


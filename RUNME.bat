@echo off
REM Upsum Project Nexus — Quick Start

REM Backend setup
cd backend
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt
start cmd /k uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd ..

REM Frontend setup
if exist frontend\package.json (
    cd frontend
    call npm install
    start cmd /k npm run dev
    cd ..
) else (
    echo Frontend directory or package.json not found. Skipping frontend start.
)

REM Open frontend in browser
start http://localhost:5173

REM Open backend docs in browser
start http://localhost:8000/docs

REM Done

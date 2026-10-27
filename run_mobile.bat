@echo off
start "LifeTimeIQ Backend" cmd /k "cd /d C:\Users\karti\OneDrive\Desktop\REAL\lifetimeiq_clv_project && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"
start "LifeTimeIQ Frontend" cmd /k "cd /d C:\Users\karti\OneDrive\Desktop\REAL\lifetimeiq_clv_project\frontend && python -m http.server 3000 --bind 0.0.0.0"
echo Both servers are now running!

import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="REBUILD AI Services Runner")
    parser.add_argument("--backend", action="store_true", help="Start FastAPI Backend Server (Port 8000)")
    parser.add_argument("--streamlit", action="store_true", help="Start Streamlit Public Demo (Port 8501)")
    parser.add_argument("--all", action="store_true", help="Start both Backend and Streamlit servers")
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(project_root)

    if not (args.backend or args.streamlit or args.all):
        args.backend = True  # Default to backend

    processes = []
    try:
        if args.backend or args.all:
            print("[REBUILD AI] Starting FastAPI Server on http://localhost:8000 ...")
            print("[REBUILD AI] API Docs: http://localhost:8000/docs")
            p_backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"])
            processes.append(p_backend)

        if args.streamlit or args.all:
            print("[REBUILD AI] Starting Streamlit Demo on http://localhost:8501 ...")
            p_streamlit = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "streamlit/app.py", "--server.port", "8501"])
            processes.append(p_streamlit)

        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n[REBUILD AI] Shutting down services...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()

import subprocess
import os
import sys
import signal
from threading import Thread
import webbrowser
import time

frontend_process = None
backend_process = None

def signal_handler(signum, frame):
    print("\n🛑 Arrêt des serveurs en cours...")
    
    if frontend_process:
        frontend_process.terminate()
        print("✅ Frontend arrêté")

    if backend_process:
        backend_process.terminate()
        print("✅ Backend arrêté")

    print("👋 Au revoir!")
    os._exit(0)

def run_frontend():
    global frontend_process
    try:
        os.chdir('frontend-web')
        if os.name == 'nt':  # Windows
            frontend_process = subprocess.Popen('npm run dev', shell=True)
        else:  # Linux/Mac
            frontend_process = subprocess.Popen(['npm', 'run', 'dev'])
    except Exception as e:
        print(f"❌ Erreur frontend: {e}")
        os._exit(1)

def run_backend():
    global backend_process
    try:
        os.chdir('backend-api')
        if os.name == 'nt': 
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
            backend_process = subprocess.Popen([python_path, '-m', 'flask', 'run'])
        else:  
            venv_python = os.path.join('venv', 'bin', 'python')
            backend_process = subprocess.Popen([venv_python, '-m', 'flask', 'run'])
    except Exception as e:
        print(f"❌ Erreur backend: {e}")
        os._exit(1)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    initial_dir = os.getcwd()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🚀 Démarrage des serveurs...")

    backend_thread = Thread(target=run_backend)
    backend_thread.start()
    print("⚙️  Backend en cours de démarrage...")
    time.sleep(2)
    
    os.chdir(initial_dir)
    
    frontend_thread = Thread(target=run_frontend)
    frontend_thread.start()
    print("🎨 Frontend en cours de démarrage...")
    time.sleep(2)

    print("🌐 Ouverture du navigateur...")
    webbrowser.open('http://localhost:5173')

    try:
        while True:
            time.sleep(1)
    except:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
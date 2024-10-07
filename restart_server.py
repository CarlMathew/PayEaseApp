import subprocess
import time
import os
import signal

def check_port_in_use(port=8000):
    """
    Checks if a given port is in use. 
    Returns a list of PIDs of the processes using the port.
    """
    try:
        # Check if the port is in use using `lsof` command
        result = subprocess.run(['sudo', 'lsof', '-t', f'-i:{port}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pids = result.stdout.decode('utf-8').strip().split('\n')  # Split by newline to get multiple PIDs
        return [int(pid) for pid in pids if pid]  # Return a list of PIDs, filtering out empty strings
    except subprocess.CalledProcessError as e:
        # If an error occurs (like no process found), return an empty list
        return []

def kill_process(pid):
    """
    Kills a process by its PID.
    """
    try:
        os.kill(pid, signal.SIGTERM)  # Gracefully terminate the process
        print(f"Terminated process {pid}.")
    except ProcessLookupError:
        print(f"Process {pid} not found.")
    except PermissionError:
        print(f"Permission denied while trying to kill process {pid}.")

def restart_django_server():
    # Set the absolute path to the project's 'payEase' directory
    project_dir = '/home/pi/Desktop/PayEaseAPP/payEase'  # Path to the 'payEase' directory

    # Absolute path to the virtual environment's python interpreter
    venv_path = os.path.join(project_dir, '..', 'venv', 'bin', 'python3')  # 'venv' is at the parent level of 'payEase'

    # Absolute path to the manage.py script
    manage_py_path = os.path.join(project_dir, 'manage.py')

    print(f"Virtual environment path: {venv_path}")  # Debugging line
    print(f"manage.py path: {manage_py_path}")  # Debugging line

    # Check if the virtual environment exists
    if not os.path.exists(venv_path):
        raise FileNotFoundError(f"Virtual environment python not found at: {venv_path}")

    # Check if manage.py exists
    if not os.path.exists(manage_py_path):
        raise FileNotFoundError(f"manage.py not found at: {manage_py_path}")

    # The port Django will use
    port = 8000

    while True:
        # Step 1: Check if the port is already in use
        pids = check_port_in_use(port)
        if pids:
            print(f"Port {port} is in use by processes {pids}. Terminating processes...")
            # Terminate all processes using the port
            for pid in pids:
                kill_process(pid)
            time.sleep(1)  # Wait briefly before restarting the server

        print("Starting Django server...")

        # Step 2: Start the Django server using the venv Python interpreter
        process = subprocess.Popen([venv_path, manage_py_path, "runserver", f"{port}"])

        try:
            # Let the server run for 1 minute (60 seconds)
            time.sleep(120)
        except KeyboardInterrupt:
            # Handle Ctrl+C to stop the process gracefully
            process.terminate()
            print("Server stopped.")
            break

        print("Restarting Django server...")

if __name__ == "__main__":
    restart_django_server()

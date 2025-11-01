import os
import subprocess
import sys

def main():
    # Set the environment variable
    os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
    
    # Clear the Streamlit cache
    print("Clearing Streamlit cache...")
    subprocess.run([sys.executable, "-m", "streamlit", "cache", "clear"], check=True)
    
    # Run the Streamlit app with the environment variable set
    print("Starting Streamlit app...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)

if __name__ == "__main__":
    main()

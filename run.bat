@echo off
setlocal

:: Set the environment variable
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

:: Clear the Streamlit cache
echo Clearing Streamlit cache...
streamlit cache clear

:: Run the app with the environment variable set
echo Starting Streamlit app...
streamlit run app.py

endlocal

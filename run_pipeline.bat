@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo  Jumbled Frame Reconstruction Pipeline
echo ========================================
echo.

:: Prompt for video path
set /p VIDEO_PATH="Enter the path to your video file: "

:: Check if video file exists
if not exist "%VIDEO_PATH%" (
    echo.
    echo [ERROR] Video file not found: %VIDEO_PATH%
    echo Please check the path and try again.
    pause
    exit /b 1
)

echo.
echo Video file: %VIDEO_PATH%
echo.

:: Prompt for FPS
set /p FPS="Enter FPS for output video (default: 30): "
if "%FPS%"=="" set FPS=30

:: Prompt for jumble option
set /p JUMBLE="Do you want to jumble frames? (y/n, default: y): "
if "%JUMBLE%"=="" set JUMBLE=y

:: Prompt for output directory
set /p OUTPUT_DIR="Enter output directory (default: output): "
if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=output

echo.
echo ========================================
echo  Pipeline Configuration
echo ========================================
echo Video File: %VIDEO_PATH%
echo FPS: %FPS%
echo Jumble Frames: %JUMBLE%
echo Output Directory: %OUTPUT_DIR%
echo ========================================
echo.

:: Build the command
set CMD=python src\run_pipeline.py --video "%VIDEO_PATH%" --fps %FPS% --output_dir "%OUTPUT_DIR%"

if /i "%JUMBLE%"=="n" (
    set CMD=!CMD! --no_jumble
)

echo Running command: !CMD!
echo.

:: Change to project directory
cd /d "%~dp0"

:: Run the pipeline
!CMD!

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Pipeline completed successfully!
    echo ========================================
    echo.
    echo Output video saved to: %OUTPUT_DIR%\reconstructed_video.mp4
    echo.
) else (
    echo.
    echo ========================================
    echo  Pipeline failed with error code: %ERRORLEVEL%
    echo ========================================
    echo.
)

pause
endlocal

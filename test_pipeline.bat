@echo off
echo ========================================
echo  Testing Pipeline with jumbled_video.mp4
echo ========================================
echo.

cd src
python run_pipeline.py --video ../data/jumbled_video.mp4 --fps 30 --output_dir ../output

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Test completed successfully!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  Test failed!
    echo ========================================
)

pause

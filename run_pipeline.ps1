# PowerShell script for running the Jumbled Frame Reconstruction Pipeline

# Function to display colored messages
function Write-ColorMessage {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Display header
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " Jumbled Frame Reconstruction Pipeline" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Prompt for video path
$videoPath = Read-Host "Enter the path to your video file"

# Check if video file exists
if (-not (Test-Path $videoPath)) {
    Write-ColorMessage "`n[ERROR] Video file not found: $videoPath" "Red"
    Write-Host "Please check the path and try again.`n"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-ColorMessage "`nVideo file found: $videoPath" "Green"

# Prompt for FPS
$fps = Read-Host "`nEnter FPS for output video (default: 30)"
if ([string]::IsNullOrWhiteSpace($fps)) {
    $fps = 30
}

# Prompt for jumble option
$jumble = Read-Host "Do you want to jumble frames? (y/n, default: y)"
if ([string]::IsNullOrWhiteSpace($jumble)) {
    $jumble = "y"
}

# Prompt for output directory
$outputDir = Read-Host "Enter output directory (default: output)"
if ([string]::IsNullOrWhiteSpace($outputDir)) {
    $outputDir = "output"
}

# Display configuration
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " Pipeline Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-ColorMessage "Video File: $videoPath" "Blue"
Write-ColorMessage "FPS: $fps" "Blue"
Write-ColorMessage "Jumble Frames: $jumble" "Blue"
Write-ColorMessage "Output Directory: $outputDir" "Blue"
Write-Host "========================================`n" -ForegroundColor Cyan

# Build the command
$cmd = "python src\run_pipeline.py --video `"$videoPath`" --fps $fps --output_dir `"$outputDir`""

if ($jumble -eq "n" -or $jumble -eq "N") {
    $cmd += " --no_jumble"
}

Write-ColorMessage "Running command: $cmd" "Yellow"
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Run the pipeline
try {
    Invoke-Expression $cmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host " Pipeline completed successfully!" -ForegroundColor Green
        Write-Host "========================================`n" -ForegroundColor Green
        Write-ColorMessage "Output video saved to: $outputDir\reconstructed_video.mp4" "Green"
        Write-Host ""
    } else {
        Write-Host "`n========================================" -ForegroundColor Red
        Write-Host " Pipeline failed with error code: $LASTEXITCODE" -ForegroundColor Red
        Write-Host "========================================`n" -ForegroundColor Red
    }
} catch {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host " Pipeline failed with error!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-ColorMessage "Error: $_" "Red"
    Write-Host ""
}

Read-Host "`nPress Enter to exit"

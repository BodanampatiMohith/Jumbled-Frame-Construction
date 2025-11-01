#!/bin/bash

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo " Jumbled Frame Reconstruction Pipeline"
echo "========================================"
echo ""

# Prompt for video path
read -p "Enter the path to your video file: " VIDEO_PATH

# Check if video file exists
if [ ! -f "$VIDEO_PATH" ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Video file not found: $VIDEO_PATH"
    echo "Please check the path and try again."
    exit 1
fi

echo ""
echo -e "${GREEN}Video file found:${NC} $VIDEO_PATH"
echo ""

# Prompt for FPS
read -p "Enter FPS for output video (default: 30): " FPS
FPS=${FPS:-30}

# Prompt for jumble option
read -p "Do you want to jumble frames? (y/n, default: y): " JUMBLE
JUMBLE=${JUMBLE:-y}

# Prompt for output directory
read -p "Enter output directory (default: output): " OUTPUT_DIR
OUTPUT_DIR=${OUTPUT_DIR:-output}

echo ""
echo "========================================"
echo " Pipeline Configuration"
echo "========================================"
echo -e "${BLUE}Video File:${NC} $VIDEO_PATH"
echo -e "${BLUE}FPS:${NC} $FPS"
echo -e "${BLUE}Jumble Frames:${NC} $JUMBLE"
echo -e "${BLUE}Output Directory:${NC} $OUTPUT_DIR"
echo "========================================"
echo ""

# Build the command
CMD="python src/run_pipeline.py --video \"$VIDEO_PATH\" --fps $FPS --output_dir \"$OUTPUT_DIR\""

if [ "$JUMBLE" = "n" ] || [ "$JUMBLE" = "N" ]; then
    CMD="$CMD --no_jumble"
fi

echo -e "${YELLOW}Running command:${NC} $CMD"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Run the pipeline
eval $CMD

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo -e " ${GREEN}Pipeline completed successfully!${NC}"
    echo "========================================"
    echo ""
    echo -e "${GREEN}Output video saved to:${NC} $OUTPUT_DIR/reconstructed_video.mp4"
    echo ""
else
    echo ""
    echo "========================================"
    echo -e " ${RED}Pipeline failed!${NC}"
    echo "========================================"
    echo ""
    exit 1
fi

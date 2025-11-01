# Pipeline Usage Guide

This guide explains how to run the Jumbled Frame Reconstruction pipeline using the provided scripts.

## Available Scripts

We provide three scripts for different platforms:

1. **run_pipeline.bat** - Windows Batch Script (CMD)
2. **run_pipeline.ps1** - Windows PowerShell Script (Recommended for Windows)
3. **run_pipeline.sh** - Unix/Linux/Mac Bash Script

## Prerequisites

Before running the pipeline, ensure you have:

1. Python 3.x installed
2. All required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
3. A video file to process

## Usage

### Windows (Batch Script)

1. Double-click `run_pipeline.bat` or run from Command Prompt:
   ```cmd
   run_pipeline.bat
   ```

2. Follow the prompts:
   - Enter the full path to your video file
   - Specify FPS (frames per second) for output video
   - Choose whether to jumble frames (y/n)
   - Specify output directory

### Windows (PowerShell Script) - Recommended

1. Right-click `run_pipeline.ps1` and select "Run with PowerShell"
   
   Or run from PowerShell:
   ```powershell
   .\run_pipeline.ps1
   ```

2. If you get an execution policy error, run PowerShell as Administrator and execute:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Follow the prompts:
   - Enter the full path to your video file
   - Specify FPS (frames per second) for output video
   - Choose whether to jumble frames (y/n)
   - Specify output directory

### Unix/Linux/Mac (Bash Script)

1. Make the script executable (first time only):
   ```bash
   chmod +x run_pipeline.sh
   ```

2. Run the script:
   ```bash
   ./run_pipeline.sh
   ```

3. Follow the prompts:
   - Enter the full path to your video file
   - Specify FPS (frames per second) for output video
   - Choose whether to jumble frames (y/n)
   - Specify output directory

## Manual Execution

You can also run the pipeline manually using Python:

```bash
cd src
python run_pipeline.py --video /path/to/your/video.mp4 --fps 30 --output_dir ../output
```

### Available Options

- `--video`: Path to the input video file (required)
- `--fps`: Frames per second for output video (default: 30)
- `--output_dir`: Directory to save the output video (default: output)
- `--no_jumble`: Skip frame jumbling (optional flag)

### Examples

**With frame jumbling:**
```bash
python run_pipeline.py --video ../data/humans_1.mp4 --fps 24 --output_dir ../results
```

**Without frame jumbling:**
```bash
python run_pipeline.py --video ../data/humans_1.mp4 --fps 30 --no_jumble
```

## Pipeline Steps

The pipeline performs the following steps:

1. **Extract Frames** - Extracts individual frames from the video
2. **Jumble Frames** (optional) - Randomly shuffles the frames
3. **Extract Features** - Uses ResNet-18 to extract visual features from each frame
4. **Build Similarity Matrix** - Computes cosine similarity between all frame pairs
5. **Solve TSP** - Uses a greedy algorithm to find the optimal frame order
6. **Rebuild Video** - Reconstructs the video with the reordered frames

## Output

The reconstructed video will be saved in the specified output directory:
- Default location: `output/reconstructed_video.mp4`
- Custom location: `<your_output_dir>/reconstructed_video.mp4`

## Troubleshooting

### Common Issues

1. **"Video file not found"**
   - Check that the path is correct
   - Use absolute paths for reliability
   - Ensure the file has a valid extension (.mp4, .avi, .mov)

2. **"Permission denied"**
   - Ensure you have write permissions in the output directory
   - Close any programs that might be using the output files

3. **"No module named..."**
   - Install dependencies: `pip install -r requirements.txt`

4. **Out of memory errors**
   - Reduce video resolution before processing
   - Process shorter video clips
   - Close other applications to free up RAM

### Getting Help

For more information, refer to the main README.md file or check the algorithm documentation in the project repository.

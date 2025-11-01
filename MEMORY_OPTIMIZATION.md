# Memory Optimization Guide

## Common Memory Issues

If you encounter "Insufficient memory" errors during pipeline execution, follow these solutions:

## Quick Fixes

### 1. Close Other Applications
Before running the pipeline:
- Close web browsers (especially Chrome/Edge with many tabs)
- Close other video/image editing software
- Close unnecessary background applications
- Restart your computer if needed

### 2. Use Smaller Videos
- Limit video length to 10-30 seconds
- Use lower resolution videos (720p instead of 1080p)
- Reduce FPS before processing

### 3. Reduce Video Size Before Processing

Use FFmpeg to reduce video size:

```bash
# Reduce resolution to 720p
ffmpeg -i input.mp4 -vf scale=1280:720 output_720p.mp4

# Reduce to 30 FPS
ffmpeg -i input.mp4 -r 30 output_30fps.mp4

# Combine both
ffmpeg -i input.mp4 -vf scale=1280:720 -r 30 output_optimized.mp4

# Reduce quality and size
ffmpeg -i input.mp4 -vf scale=854:480 -r 24 -crf 28 output_small.mp4
```

## Memory Optimization Already Implemented

The pipeline now includes:

### 1. Batched Processing
- Processes frames in batches of 50
- Runs garbage collection after each batch
- Clears GPU cache (if using CUDA)

### 2. Image Resizing
- Automatically resizes large images before processing
- Limits max resolution to 1920x1080

### 3. Error Handling
- Gracefully handles memory errors
- Skips problematic frames instead of crashing
- Reports failed frames at the end

### 4. Explicit Memory Cleanup
- Deletes temporary frame data immediately after use
- Runs Python garbage collector periodically
- Releases OpenCV resources properly

## System Requirements

### Minimum:
- **RAM**: 4 GB
- **Video**: Up to 30 seconds, 720p
- **Frames**: Up to 300 frames

### Recommended:
- **RAM**: 8 GB or more
- **Video**: Up to 60 seconds, 1080p
- **Frames**: Up to 600 frames
- **GPU**: NVIDIA GPU with CUDA support (optional but faster)

## Troubleshooting Specific Errors

### "Failed to allocate X bytes"
**Cause**: System running out of RAM

**Solutions**:
1. Restart your computer
2. Close all unnecessary applications
3. Use a smaller/shorter video
4. Reduce video resolution using FFmpeg

### "OpenCV error: Insufficient memory"
**Cause**: Large image files causing memory overflow

**Solutions**:
1. The pipeline now automatically resizes large images
2. If still failing, manually reduce video resolution before processing
3. Process fewer frames (trim video duration)

### "No features extracted! All frames failed"
**Cause**: All frames failed to load due to memory/corruption

**Solutions**:
1. Check if video file is corrupted
2. Try converting video to a different format
3. Ensure enough disk space for temporary frames

## Performance Tips

### 1. Use GPU if Available
If you have an NVIDIA GPU with CUDA:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 2. Process in Stages
For very large videos, you can manually process in stages:

```bash
# Stage 1: Extract & Jumble
python src/extract_frames.py
python src/jumble_frames.py

# Free up memory, close applications

# Stage 2: Features & TSP
python src/feature_extraction.py
python src/build_similarity.py
python src/tsp_solver.py

# Free up memory again

# Stage 3: Rebuild
python src/rebuild_video.py
```

### 3. Monitor Memory Usage

**Windows:**
- Task Manager > Performance > Memory

**Linux/Mac:**
- `htop` or `top` command

Keep memory usage below 80% while running the pipeline.

## Video Size Guidelines

| Resolution | Duration | Approx RAM Needed | Status |
|------------|----------|-------------------|---------|
| 480p | 30 sec | 2-3 GB | ✅ Safe |
| 720p | 30 sec | 3-4 GB | ✅ Safe |
| 1080p | 30 sec | 4-6 GB | ⚠️ Check RAM |
| 1080p | 60 sec | 6-8 GB | ⚠️ Requires 8GB+ |
| 1440p | 30 sec | 6-8 GB | ⚠️ May fail |
| 4K | Any | 10+ GB | ❌ Not recommended |

## Emergency Solutions

If you absolutely need to process a large video:

### Option 1: Split the Video
```bash
# Split into 2 parts
ffmpeg -i input.mp4 -t 00:00:30 -c copy part1.mp4
ffmpeg -i input.mp4 -ss 00:00:30 -c copy part2.mp4

# Process each part separately
# Merge results afterward
```

### Option 2: Extract Fewer Frames
Modify `extract_frames.py` to extract every Nth frame:
```python
# In extract_frames.py, change the loop:
skip_frames = 2  # Extract every 2nd frame
idx = 0
frame_num = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_num % skip_frames == 0:
        # Save frame
        idx += 1
    frame_num += 1
```

### Option 3: Cloud Processing
Use cloud services with more RAM:
- Google Colab (free, up to 12 GB RAM)
- AWS EC2 (paid, configurable)
- Paperspace (paid, GPU available)

## Need More Help?

If you continue experiencing memory issues:
1. Check your system specs (RAM, available disk space)
2. Verify video file isn't corrupted
3. Try with a very short test video (5-10 seconds)
4. Report the issue with your system specs and video details

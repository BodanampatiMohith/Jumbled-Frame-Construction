# Changelog - Jumbled Frame Reconstruction Pipeline

## Recent Fixes (2024-11-01)

### Issue: Old Video Frames Being Processed
**Problem:** The pipeline was processing old frames from previous runs instead of only the new video file, causing:
- Frame count mismatches (250 new + 300 old = 600 total)
- Many "frame index out of range" errors
- Incorrect video reconstruction

**Root Cause:**
1. Old frame directories were not being cleared between runs
2. Base directory path was pointing to `src/` instead of project root
3. Leftover intermediate files (features, similarity matrix) from previous runs

**Solution:**
1. **Added cleanup step** in `run_pipeline.py` that clears:
   - `data/frames/` directory
   - `data/frames_jumbled/` directory
   - Old feature files (`frame_features.npy`)
   - Old similarity matrix (`similarity_matrix.npy`)
   - Old frame order file (`frame_order_final.npy`)

2. **Fixed base directory path**:
   - Changed from: `base_dir = Path(__file__).parent` (points to `src/`)
   - Changed to: `base_dir = Path(__file__).parent.parent` (points to project root)

3. **Added output directory handling**:
   - Makes output directory absolute if it's specified as relative
   - Ensures output goes to the correct location

### Files Modified

#### `src/run_pipeline.py`
- Fixed `base_dir` to point to project root instead of `src/` directory
- Added cleanup logic to remove old frames and intermediate files before processing
- Improved output directory path handling

#### `src/jumble_frames.py`
- Added directory clearing before jumbling (safety measure)
- Prevents mixing old and new jumbled frames

### New Features

#### Interactive Scripts Created
1. **`run_pipeline.bat`** - Windows Batch script
2. **`run_pipeline.ps1`** - Windows PowerShell script (recommended)
3. **`run_pipeline.sh`** - Unix/Linux/Mac Bash script

All scripts:
- Prompt for video file path (no hardcoded paths)
- Ask for FPS settings
- Option to enable/disable frame jumbling
- Custom output directory support
- Colored output and error messages
- File existence validation

#### Documentation
- **`PIPELINE_USAGE.md`** - Complete usage guide with examples
- **`CHANGELOG.md`** - This file

## Usage Example

### Using Interactive Scripts (Recommended)

**Windows PowerShell:**
```powershell
.\run_pipeline.ps1
```

**Windows CMD:**
```cmd
run_pipeline.bat
```

**Linux/Mac:**
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### Manual Execution

```bash
cd src
python run_pipeline.py --video /path/to/your/video.mp4 --fps 30 --output_dir ../output
```

## Expected Pipeline Behavior (After Fix)

1. **Cleanup Phase:**
   ```
   🧹 Cleaning old directories and files...
      Cleared: data/frames
      Cleared: data/frames_jumbled
      Deleted: frame_features.npy
      Deleted: similarity_matrix.npy
      Deleted: frame_order_final.npy
   ```

2. **Frame Extraction:**
   ```
   1️⃣ Extracting frames...
   Total frames: 250
   ✅ Extracted 250 frames to data/frames
   ```

3. **Frame Jumbling:**
   ```
   2️⃣ Jumbling frames...
   Found 250 frames in data/frames  ← Should match extracted count
   ✅ Successfully jumbled 250 frames
   ```

4. **Feature Extraction:**
   ```
   3️⃣ Extracting features...
   Extracting features: 100%|███████| 250/250  ← Should match frame count
   ✅ Saved feature vectors to data/frame_features.npy
   ```

5. **Similarity Matrix:**
   ```
   4️⃣ Building similarity matrix...
   Matrix shape: (250, 250)  ← Should be N×N where N is frame count
   ```

6. **TSP Solving:**
   ```
   5️⃣ Solving optimal frame order...
   🔍 Finding optimal path through 250 frames  ← Should match frame count
   ```

7. **Video Reconstruction:**
   ```
   6️⃣ Reconstructing video...
   Processed 250/250 frames  ← No "out of range" errors
   ✅ Success! Video saved to: output/reconstructed_video.mp4
   ```

## Verification Checklist

After running the pipeline, verify:
- [ ] Frame count matches throughout all steps
- [ ] No "frame index out of range" warnings
- [ ] Output video file size is reasonable
- [ ] Output video plays correctly
- [ ] Only one video in the output directory

## Known Limitations

1. **Feature extraction is slow on CPU** - Consider using GPU if available
2. **Large videos may run out of memory** - Consider processing shorter clips or reducing resolution
3. **FFmpeg warnings** - Some codec warnings are normal and don't affect output

## Future Improvements

- [ ] Add GPU acceleration support detection
- [ ] Add progress saving/resuming for long videos
- [ ] Optimize memory usage for large videos
- [ ] Add video preview in the terminal
- [ ] Support for multiple video formats

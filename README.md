# Jumbled Frame Reconstruction

[![GitHub stars](https://img.shields.io/github/stars/BodanampatiMohith/Jumbled-Frame-Construction?style=social)](https://github.com/BodanampatiMohith/Jumbled-Frame-Construction/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/BodanampatiMohith/Jumbled-Frame-Construction)](https://github.com/BodanampatiMohith/Jumbled-Frame-Construction/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Algorithm](https://img.shields.io/badge/Algorithm-Documentation-blue)](https://github.com/BodanampatiMohith/Jumbled-Frame-Construction/blob/main/algo.md)

A machine learning pipeline for reconstructing the original sequence of frames from jumbled videos using deep learning and optimization techniques. This project employs ResNet-18 for feature extraction and a greedy Traveling Salesman Problem (TSP) solver to determine the optimal frame ordering.

## Overview

This system automatically analyzes scrambled video frames, extracts visual features using a pre-trained convolutional neural network, computes frame-to-frame similarity, and reconstructs the original temporal sequence. Applications include video forensics, data recovery, video restoration, and educational demonstrations of computer vision techniques.

## Key Features

- **Automated Pipeline**: Single-command execution via interactive scripts (PowerShell, Bash, CMD)
- **Deep Learning Feature Extraction**: Utilizes pre-trained ResNet-18 for robust visual feature representation
- **Intelligent Frame Ordering**: Greedy TSP algorithm for optimal sequence reconstruction
- **Flexible FPS Support**: Automatic detection and preservation of original video frame rate (supports 24, 30, 60, 120+ FPS)
- **Memory Optimization**: Batch processing with automatic garbage collection for handling large videos
- **Cross-Platform**: Compatible with Windows, Linux, and macOS
- **Optional Frame Scrambling**: Built-in frame jumbling for testing and demonstration

## System Requirements

**Minimum:**
- Python 3.7 or higher
- 4 GB RAM
- 2 GB free disk space

**Recommended:**
- Python 3.8+
- 8 GB RAM or higher
- NVIDIA GPU with CUDA support (optional, significantly faster)
- 5 GB free disk space

**Dependencies:**
- PyTorch >= 1.9.0
- torchvision >= 0.10.0
- OpenCV (opencv-python) >= 4.5.0
- NumPy >= 1.19.0
- scikit-learn >= 0.24.0
- tqdm >= 4.60.0

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/BodanampatiMohith/Jumbled-Frame-Construction.git
   cd Jumbled-Frame-Construction
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) GPU Support**
   
   For CUDA-enabled GPU acceleration:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

## Usage

### Quick Start (Interactive Mode)

**Windows (PowerShell - Recommended)**
```powershell
.\run_pipeline.ps1
```

**Windows (Command Prompt)**
```cmd
run_pipeline.bat
```

**Linux/macOS**
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

The interactive script will prompt you for:
- Video file path
- Output FPS (optional, defaults to original video FPS)
- Whether to jumble frames before processing
- Output directory location

### Command-Line Usage

**Basic Usage (Auto-detect FPS)**
```bash
python src/run_pipeline.py --video path/to/video.mp4
```

**With Custom FPS**
```bash
python src/run_pipeline.py --video path/to/video.mp4 --fps 60
```

**Without Frame Jumbling**
```bash
python src/run_pipeline.py --video path/to/video.mp4 --no_jumble
```

**Full Options**
```bash
python src/run_pipeline.py --video path/to/video.mp4 --fps 30 --output_dir results --no_jumble
```

### Manual Step-by-Step Execution

For fine-grained control, run individual pipeline stages:

```bash
# Step 1: Extract frames
python src/extract_frames.py

# Step 2: Jumble frames (optional)
python src/jumble_frames.py

# Step 3: Extract features
python src/feature_extraction.py

# Step 4: Build similarity matrix
python src/build_similarity.py

# Step 5: Solve frame ordering
python src/tsp_solver.py

# Step 6: Reconstruct video
python src/rebuild_video.py
```

### Output

- **Reconstructed Video**: `output/reconstructed_video.mp4`
- **Extracted Frames**: `data/frames/`
- **Jumbled Frames**: `data/frames_jumbled/`
- **Feature Vectors**: `data/features/frame_features.npy`
- **Similarity Matrix**: `data/similarity_matrix.npy`
- **Frame Order**: `data/frame_order_final.npy`
- **Video Metadata**: `data/video_metadata.json`

## Project Structure

```
Jumbled-Frame-Construction/
├── data/                       # Data directory
│   ├── frames/                 # Extracted video frames
│   ├── frames_jumbled/         # Scrambled frames
│   ├── features/               # Feature vectors
│   │   └── frame_features.npy
│   ├── similarity_matrix.npy   # Frame similarity scores
│   ├── frame_order_final.npy   # Reconstructed frame sequence
│   └── video_metadata.json     # Video properties (FPS, resolution)
├── output/                     # Reconstructed videos
│   └── reconstructed_video.mp4
├── src/                        # Source code
│   ├── extract_frames.py       # Frame extraction module
│   ├── jumble_frames.py        # Frame scrambling module
│   ├── feature_extraction.py   # ResNet-18 feature extraction
│   ├── build_similarity.py     # Cosine similarity computation
│   ├── tsp_solver.py           # Greedy TSP solver
│   ├── rebuild_video.py        # Video reconstruction
│   └── run_pipeline.py         # Automated pipeline orchestration
├── run_pipeline.ps1            # PowerShell interactive script
├── run_pipeline.bat            # Windows CMD interactive script
├── run_pipeline.sh             # Bash interactive script
├── requirements.txt            # Python dependencies
├── algo.md                     # Algorithm documentation
└── README.md                   # Project documentation
```

## Algorithm Details

The reconstruction pipeline employs a multi-stage approach:

1. **Frame Extraction**: Decomposes video into individual frames with metadata preservation
2. **Feature Extraction**: ResNet-18 (pre-trained on ImageNet) generates 512-dimensional feature vectors per frame
3. **Similarity Computation**: Cosine similarity matrix (NxN) computed for all frame pairs
4. **Sequence Optimization**: Greedy TSP algorithm identifies optimal frame ordering by maximizing sequential similarity
5. **Video Synthesis**: Frames reassembled into video format with original or specified FPS

For detailed algorithm documentation, see [algo.md](algo.md).

## Performance Metrics

Benchmark results on standard test videos:

- **Mean Sequential Similarity**: 98.30%
- **Minimum Similarity**: 89.04%
- **Maximum Similarity**: 99.87%
- **Processing Speed**: ~8-10 frames/second (CPU), ~50-60 frames/second (GPU)
- **Memory Usage**: ~4-6 GB for 1080p 30-second videos

## Supported Video Formats

- **Input**: MP4, AVI, MOV, MKV, FLV, WMV
- **Output**: MP4 (H.264 codec)
- **Resolution**: Up to 4K (memory permitting)
- **Frame Rate**: Any (24, 29.97, 30, 59.94, 60, 120+ FPS)

## Troubleshooting

**Memory Errors**
- Reduce video resolution or duration
- Close unnecessary applications
- Use smaller batch sizes in feature extraction

**Slow Processing**
- Install CUDA-enabled PyTorch for GPU acceleration
- Reduce video resolution before processing
- Use lower frame rate videos

**Frame Count Mismatch**
- Pipeline automatically cleans old frames between runs
- Check `data/` directory for leftover files if issues persist

## Contributing

Contributions are welcome. Please submit pull requests with:
- Clear description of changes
- Updated documentation
- Test results for new features

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use this project in academic work, please cite:

```bibtex
@software{jumbled_frame_reconstruction,
  author = {Bodanampati Mohith},
  title = {Jumbled Frame Reconstruction},
  year = {2024},
  url = {https://github.com/BodanampatiMohith/Jumbled-Frame-Construction}
}
```

## Acknowledgments

- ResNet-18 architecture from PyTorch torchvision
- OpenCV library for video processing
- scikit-learn for cosine similarity computation

## Contact

- GitHub: [@BodanampatiMohith](https://github.com/BodanampatiMohith)
- Issues: [GitHub Issues](https://github.com/BodanampatiMohith/Jumbled-Frame-Construction/issues)

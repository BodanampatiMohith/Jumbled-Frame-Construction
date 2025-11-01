<<<<<<< HEAD
# Jumbled-Frame-Construction
=======
# Jumbled Frame Reconstruction

[![GitHub stars](https://img.shields.io/github/stars/BodanampatiMohith/Jumbled-Frame-Construction?style=social)](https://github.com/BodanampatiMohith/Jumbled-Frame-Construction/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/BodanampatiMohith/Jumbled-Frame-Construction)](https://github.com/BodanampatiMohith/Jumbled-Frame-Construction/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Reconstruct the original sequence of frames from a jumbled video using computer vision and machine learning. This project is particularly useful for video restoration, forensic analysis, and educational purposes.

This project implements a pipeline to reconstruct the original sequence of frames from a jumbled video using computer vision and machine learning techniques. It's particularly useful for video restoration, forensic analysis, and educational purposes.

## 🚀 Features

- Extracts frames from input videos
- Jumbles frames for processing
- Uses ResNet-18 for feature extraction
- Reconstructs original sequence using TSP (Traveling Salesman Problem)
- Generates a smooth output video

## 📋 Prerequisites

- Python 3.7+
- OpenCV (`pip install opencv-python`)
- PyTorch (`pip install torch torchvision`)
- NumPy (`pip install numpy`)
- scikit-learn (`pip install scikit-learn`)
- tqdm (`pip install tqdm`)

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BodanampatiMohith/Jumbled-Frame-Construction.git
   cd Jumbled-Frame-Construction
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🎬 Usage

1. **Prepare Your Video**
   - Place your video file in the `data` directory
   - Supported formats: .mp4, .avi, .mov

2. **Configure the Pipeline**
   - Update the video filename in `src/extract_frames.py` (line 30)
   - Adjust parameters in other scripts if needed (FPS, resolution, etc.)

3. **Run the Pipeline**
   ```bash
   # Extract frames from video
   python src/extract_frames.py
   
   # Jumble frames (optional)
   python src/jumble_frames.py
   
   # Extract features using ResNet-18
   python src/feature_extraction.py
   
   # Build similarity matrix
   python src/build_similarity.py
   
   # Solve for optimal frame order
   python src/tsp_solver.py
   
   # Reconstruct the final video
   python src/rebuild_video.py
   ```

4. **Output**
   - Find the reconstructed video in the `output` directory
   - Check `data/` for intermediate files and visualizations

## 📁 Project Structure

```
jumbled-reconstruction/
├── data/                   # Input/Output data
│   ├── frames/             # Extracted frames
│   ├── frames_jumbled/     # Jumbled frames
│   ├── frame_features.npy  # Extracted features
│   └── similarity_matrix.npy
├── output/                 # Reconstructed videos
├── src/                    # Source code
│   ├── extract_frames.py
│   ├── jumble_frames.py
│   ├── feature_extraction.py
│   ├── build_similarity.py
│   ├── tsp_solver.py
│   └── rebuild_video.py
└── README.md
```

## 📊 Performance Metrics

- **Mean Frame Similarity**: 99.06%
- **Minimum Similarity**: 66.87%
- **Maximum Similarity**: 100.00%

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ResNet-18 model for feature extraction
- OpenCV for video processing
- scikit-learn for similarity calculations
>>>>>>> 466a2d8 (Initial commit: ML-based Jumbled Frame Reconstruction pipeline with CUDA and batching support)

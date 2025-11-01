import os
import sys
import importlib
import base64

# Workaround for PyTorch and Streamlit file watcher conflict
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

import streamlit as st
import time

# Store pipeline functions to be loaded lazily
pipeline_functions = {}

def lazy_import_functions():
    """Lazily import pipeline functions when needed."""
    try:
        from src.extract_frames import extract_frames
        from src.jumble_frames import jumble_frames
        from src.feature_extraction import extract_features
        from src.build_similarity import build_similarity
        from src.tsp_solver import solve_tsp
        from src.rebuild_video import rebuild_video
        
        return {
            'extract_frames': extract_frames,
            'jumble_frames': jumble_frames,
            'extract_features': extract_features,
            'build_similarity': build_similarity,
            'solve_tsp': solve_tsp,
            'rebuild_video': rebuild_video
        }
    except ImportError as e:
        st.error(f"Error importing pipeline modules: {str(e)}")
        st.stop()
        return {}

# Page config
st.set_page_config(
    page_title="Jumbled Frame Reconstruction",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .progress-bar {
        height: 20px;
        background-color: #f0f0f0;
        border-radius: 10px;
        margin: 10px 0;
    }
    .progress-bar-fill {
        height: 100%;
        background-color: #4CAF50;
        border-radius: 10px;
        width: 0%;
        transition: width 0.3s ease;
    }
    .status-box {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        background-color: #f8f9fa;
        border-left: 5px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎬 Jumbled Frame Reconstruction")
st.markdown("""
Reconstruct the original sequence of frames from a jumbled video using computer vision and machine learning.
""")

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    
    # Processing options
    st.subheader("Processing Options")
    jumble_frames_option = st.checkbox("Jumble frames before processing", value=True)
    
    # Advanced options
    with st.expander("Advanced Options"):
        fps = st.slider("Frames per second (FPS)", 1, 60, 30)
        resolution_scale = st.slider("Resolution scale", 0.1, 1.0, 0.5)
        
    # Process button
    process_btn = st.button("Start Processing")

def ensure_directories():
    """Ensure all required directories exist."""
    os.makedirs("data/frames", exist_ok=True)
    os.makedirs("data/frames_jumbled", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("data/features", exist_ok=True)

# Initialize lazy-loaded functions when needed
def get_pipeline_functions():
    if not pipeline_functions:
        pipeline_functions.update(lazy_import_functions())
    return pipeline_functions

# Main content area
if uploaded_file is not None:
    # Ensure all required directories exist
    ensure_directories()
    
    # Save uploaded file
    video_path = os.path.join("data", uploaded_file.name)
    os.makedirs("data", exist_ok=True)
    
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display video with better error handling
    st.subheader("Uploaded Video Preview")
    
    # Create a temporary file with a unique name
    import tempfile
    
    # Create a temporary directory if it doesn't exist
    temp_dir = os.path.join(os.getcwd(), "temp_preview")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Create a temporary file with .mp4 extension
    temp_video_path = os.path.join(temp_dir, "preview.mp4")
    
    try:
        # Save the uploaded file
        with open(temp_video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display the video using st.video with the file path
        st.video(temp_video_path)
        
        # Add download button
        with open(temp_video_path, "rb") as f:
            st.download_button(
                "Download Original Video",
                data=f,
                file_name=uploaded_file.name,
                mime="video/mp4"
            )
        
    except Exception as e:
        st.error(f"Could not display video preview: {str(e)}")
        st.warning("The video file might be in an unsupported format. The processing will continue, but the preview might not work.")
        
    finally:
        # Clean up the temporary file
        try:
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
        except:
            pass
    
    # Processing section
    if process_btn:
        st.subheader("🔄 Processing Pipeline")
        
        # Initialize progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Get pipeline functions
            pipeline = get_pipeline_functions()
            
            # Step 1: Extract frames
            status_text.markdown("### 🔄 Step 1/6: Extracting frames...")
            output_dir = os.path.join("data", "frames")
            pipeline['extract_frames'](video_path, output_dir)
            progress_bar.progress(16)
            
            # Step 2: Jumble frames (if enabled)
            if jumble_frames_option:
                status_text.markdown("### 🔄 Step 2/6: Jumbling frames...")
                pipeline['jumble_frames']()
            else:
                status_text.markdown("### ⏩ Skipping frame jumbling")
                # If not jumbling, make sure frames_jumbled directory exists
                frames_dir = os.path.join("data", "frames")
                frames_jumbled_dir = os.path.join("data", "frames_jumbled")
                if not os.path.exists(frames_jumbled_dir):
                    import shutil
                    if os.path.exists(frames_dir):
                        shutil.copytree(frames_dir, frames_jumbled_dir)
            progress_bar.progress(32)
            
            # Step 3: Extract features
            status_text.markdown("### 🔄 Step 3/6: Extracting features...")
            frames_dir = os.path.join("data", "frames_jumbled" if jumble_frames_option else "frames")
            output_path = os.path.join("data", "frame_features.npy")
            pipeline['extract_features'](frames_dir, output_path)
            progress_bar.progress(48)
            
            # Step 4: Build similarity matrix
            status_text.markdown("### 🔄 Step 4/6: Building similarity matrix...")
            pipeline['build_similarity']()
            progress_bar.progress(64)
            
            # Step 5: Solve TSP
            status_text.markdown("### 🔄 Step 5/6: Solving optimal frame order...")
            pipeline['solve_tsp']()
            progress_bar.progress(80)
            
            # Step 6: Rebuild video
            status_text.markdown("### 🔄 Step 6/6: Reconstructing video...")
            pipeline['rebuild_video']()
            progress_bar.progress(100)
            
            # Display result
            st.success("✅ Processing complete!")
            
            # Show result
            st.subheader("🎥 Reconstructed Video")
            output_video = os.path.join("output", "reconstructed_video.mp4")
            
            try:
                if os.path.exists(output_video):
                    # Display video with better error handling
                    video_bytes = open(output_video, 'rb').read()
                    st.video(video_bytes, format='video/mp4', start_time=0)
                    
                    # Add download button
                    st.download_button(
                        label="⬇️ Download Reconstructed Video",
                        data=video_bytes,
                        file_name="reconstructed_video.mp4",
                        mime="video/mp4"
                    )
                    
                    # Show video info
                    video_size = os.path.getsize(output_video) / (1024 * 1024)  # in MB
                    st.info(f"Video size: {video_size:.2f} MB")
                    
                else:
                    st.error("Failed to generate output video. Please check the console for errors.")
            except Exception as e:
                st.error(f"Error displaying video: {str(e)}")
                if os.path.exists(output_video):
                    st.download_button(
                        label="⬇️ Download Video (Preview Unavailable)",
                        data=open(output_video, 'rb'),
                        file_name="reconstructed_video.mp4",
                        mime="video/mp4"
                    )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

# Add some empty space at the bottom
for _ in range(5):
    st.write("")

# Footer
st.markdown("---")
st.markdown("### 🛠️ Jumbled Frame Reconstruction Tool")
st.markdown("Built with ❤️ using Streamlit")

# Add requirements to requirements.txt if not already present
requirements = [
    "streamlit==1.32.0",
    "opencv-python-headless>=4.5.0",
    "torch>=1.9.0",
    "torchvision>=0.10.0",
    "numpy>=1.19.0",
    "scikit-learn>=0.24.0",
    "tqdm>=4.60.0"
]

# Check and update requirements.txt
req_file = "requirements.txt"
if not os.path.exists(req_file):
    with open(req_file, "w") as f:
        for req in requirements:
            f.write(f"{req}\n")
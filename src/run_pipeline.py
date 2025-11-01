import os
import sys
import argparse
from pathlib import Path

def run_pipeline(video_path, output_dir="output", jumble_frames=True, fps=30):
    """
    Run the complete video reconstruction pipeline.
    
    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save the output video.
        jumble_frames (bool): Whether to jumble frames before processing.
        fps (int): Frames per second for the output video.
    """
    # Ensure all required directories exist
    base_dir = Path(__file__).parent.parent  # Go up to project root (not src/)
    data_dir = base_dir / "data"
    frames_dir = data_dir / "frames"
    frames_jumbled_dir = data_dir / "frames_jumbled"
    features_dir = data_dir / "features"
    
    # Make output_dir absolute if it's relative
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = base_dir / output_dir
    
    for dir_path in [frames_dir, frames_jumbled_dir, features_dir, output_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    print("🚀 Starting video reconstruction pipeline...")
    
    try:
        # Clear old intermediate files only
        import shutil
        print("\n🧹 Cleaning old processing files...")
        old_files = [
            data_dir / "frame_features.npy",
            data_dir / "similarity_matrix.npy",
            data_dir / "frame_order_final.npy"
        ]
        for old_file in old_files:
            if old_file.exists():
                old_file.unlink()
                print(f"   Deleted: {old_file.name}")
        
        # Step 1: Extract frames (it will clear frames directory)
        print("\n1️⃣ Extracting frames...")
        from extract_frames import extract_frames
        extract_frames(str(video_path), str(frames_dir))
        
        if jumble_frames:
            # Step 2: Jumble frames
            print("\n2️⃣ Jumbling frames...")
            from jumble_frames import jumble_frames
            jumble_frames()
            frames_to_process = frames_jumbled_dir
        else:
            frames_to_process = frames_dir
        
        # Step 3: Extract features
        print("\n3️⃣ Extracting features...")
        from feature_extraction import extract_features
        features_path = features_dir / "frame_features.npy"
        extract_features(str(frames_to_process), str(features_path))
        
        # Step 4: Build similarity matrix
        print("\n4️⃣ Building similarity matrix...")
        from build_similarity import build_similarity
        build_similarity()
        
        # Step 5: Solve TSP
        print("\n5️⃣ Solving optimal frame order...")
        from tsp_solver import solve_tsp
        solve_tsp()
        
        # Step 6: Rebuild video
        print("\n6️⃣ Reconstructing video...")
        from rebuild_video import rebuild_video
        rebuild_video()
        
        print(f"\n✅ Pipeline completed successfully!")
        print(f"   Output video saved to: {output_dir / 'reconstructed_video.mp4'}")
        
    except Exception as e:
        print(f"\n❌ Error in pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the complete video reconstruction pipeline.")
    parser.add_argument("--video", type=str, required=True, help="Path to the input video file")
    parser.add_argument("--output_dir", type=str, default="output", help="Directory to save the output video")
    parser.add_argument("--no_jumble", action="store_true", help="Skip frame jumbling")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for the output video")
    
    args = parser.parse_args()
    
    run_pipeline(
        video_path=args.video,
        output_dir=args.output_dir,
        jumble_frames=not args.no_jumble,
        fps=args.fps
    )
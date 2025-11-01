import cv2
import os
from tqdm import tqdm

def extract_frames(video_path, output_dir):
    # Clear the output directory if it exists
    import shutil
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {total_frames}")

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"frame_{idx:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        idx += 1

    cap.release()
    print(f"✅ Extracted {idx} frames to {output_dir}")

if __name__ == "__main__":
    import os
 
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    video_filename = 'humans_1.mp4'
    
    video_path = os.path.join(base_dir, 'data', video_filename)
    output_dir = os.path.join(base_dir, 'data', 'frames')

    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🔍 Looking for video at: {video_path}")
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found at {video_path}")
        print("Please make sure to place your video file in the data directory.")
        exit(1)
        
    print(f"📁 Output frames will be saved to: {output_dir}")
    print("⏳ Starting frame extraction...")
    extract_frames(video_path, output_dir)

import cv2
import os
from tqdm import tqdm

def extract_frames(video_path, output_dir):
    # Clear the output directory if it exists
    import shutil
    import json
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"📹 Video Info:")
    print(f"  - Total frames: {total_frames}")
    print(f"  - FPS: {fps:.2f}")
    print(f"  - Resolution: {width}x{height}")

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"frame_{idx:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        idx += 1

    cap.release()
    
    # Save video metadata for later use
    metadata = {
        'fps': fps,
        'width': width,
        'height': height,
        'total_frames': idx
    }
    
    base_dir = os.path.dirname(os.path.dirname(output_dir))
    metadata_path = os.path.join(base_dir, 'data', 'video_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Extracted {idx} frames to {output_dir}")
    print(f"📝 Saved video metadata (FPS: {fps:.2f})")
    
    return fps, width, height

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

import os
import random
import shutil

def jumble_frames():
    # Get the base directory (one level up from src)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define input and output directories
    input_dir = os.path.join(base_dir, 'data', 'frames')
    output_dir = os.path.join(base_dir, 'data', 'frames_jumbled')
    
    # Create output directory if it doesn't exist, clear it if it does
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files from input directory
    frames = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(frames)} frames in {input_dir}")
    
    if not frames:
        print("❌ No frames found in the input directory!")
        return
    
    # Shuffle the frames
    random.shuffle(frames)
    
    # Copy frames to output directory with new names
    for i, frame in enumerate(frames):
        src = os.path.join(input_dir, frame)
        dst = os.path.join(output_dir, f"{i:04d}.jpg")
        shutil.copy2(src, dst)
    
    print(f"✅ Successfully jumbled {len(frames)} frames")
    print(f"Jumbled frames saved to: {output_dir}")

if __name__ == "__main__":
    jumble_frames()

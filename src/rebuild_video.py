import cv2
import numpy as np
import os

def rebuild_video():
    # Get the base directory (one level up from src)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define file paths
    frames_dir = os.path.join(base_dir, 'data', 'frames_jumbled')
    order_path = os.path.join(base_dir, 'data', 'frame_order_final.npy')
    output_dir = os.path.join(base_dir, 'output')
    output_path = os.path.join(output_dir, 'reconstructed_video.mp4')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎞️ Loading frame order...")
    if not os.path.exists(order_path):
        print(f"❌ Frame order file not found: {order_path}")
        print("Please run tsp_solver.py first to generate the frame order.")
        return
        
    order = np.load(order_path)
    print(f"  - Total frames in order: {len(order)}")

    # Get list of frame files
    frame_files = [f for f in os.listdir(frames_dir) 
                  if f.endswith(('.jpg', '.jpeg', '.png'))]
    frame_files.sort()  # Important to maintain consistent ordering
    
    if not frame_files:
        print(f"❌ No frame files found in {frames_dir}")
        return
        
    print(f"  - Found {len(frame_files)} frame files")

    # Get video properties from first frame
    first_frame_path = os.path.join(frames_dir, frame_files[0])
    first_frame = cv2.imread(first_frame_path)
    if first_frame is None:
        print(f"❌ Could not read frame: {first_frame_path}")
        return
        
    height, width, _ = first_frame.shape
    fps = 30  # Frames per second
    
    print(f"\n🎥 Video Properties:")
    print(f"  - Resolution: {width}x{height}")
    print(f"  - FPS: {fps}")
    print(f"  - Duration: {len(order)/fps:.2f} seconds")
    print(f"\n🛠️ Reconstructing video...")

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Write frames in the determined order
    for i, frame_idx in enumerate(order):
        if frame_idx >= len(frame_files):
            print(f"⚠️ Frame index {frame_idx} out of range. Skipping...")
            continue
            
        frame_path = os.path.join(frames_dir, frame_files[frame_idx])
        frame = cv2.imread(frame_path)
        
        if frame is None:
            print(f"⚠️ Could not read frame {frame_path}. Skipping...")
            continue
            
        out.write(frame)
        
        # Show progress
        if (i + 1) % 50 == 0 or (i + 1) == len(order):
            print(f"  - Processed {i + 1}/{len(order)} frames...")
    
    # Release video writer
    out.release()
    
    # Verify the output file was created
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # in MB
        print(f"\n✅ Success! Video saved to: {output_path}")
        print(f"   - File size: {file_size:.2f} MB")
        print(f"   - Resolution: {width}x{height}")
        print(f"   - Frames: {len(order)}")
        print(f"   - Duration: {len(order)/fps:.2f} seconds")
    else:
        print("❌ Failed to create output video file.")

if __name__ == "__main__":
    rebuild_video()

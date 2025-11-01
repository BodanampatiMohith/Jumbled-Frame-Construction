import cv2
import numpy as np
import os
import gc
import json

def rebuild_video(fps=None):
    """
    Rebuild video from frames in the determined order.
    
    Args:
        fps: Frames per second for output video. If None, uses original video FPS from metadata.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    frames_dir = os.path.join(base_dir, 'data', 'frames_jumbled')
    order_path = os.path.join(base_dir, 'data', 'frame_order_final.npy')
    output_dir = os.path.join(base_dir, 'output')
    output_path = os.path.join(output_dir, 'reconstructed_video.mp4')
    metadata_path = os.path.join(base_dir, 'data', 'video_metadata.json')
    
    # Load video metadata if available
    if fps is None and os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                fps = metadata.get('fps', 30)
                print(f"📝 Using original video FPS from metadata: {fps:.2f}")
        except:
            fps = 30
            print(f"⚠️ Could not read metadata, defaulting to FPS: {fps}")
    elif fps is None:
        fps = 30
        print(f"⚠️ No FPS specified and no metadata found, defaulting to: {fps}")
 
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎞️ Loading frame order...")
    if not os.path.exists(order_path):
        print(f"❌ Frame order file not found: {order_path}")
        print("Please run tsp_solver.py first to generate the frame order.")
        return
        
    order = np.load(order_path)
    print(f"  - Total frames in order: {len(order)}")

    frame_files = [f for f in os.listdir(frames_dir) 
                  if f.endswith(('.jpg', '.jpeg', '.png'))]
    frame_files.sort() 
    
    if not frame_files:
        print(f"❌ No frame files found in {frames_dir}")
        return
        
    print(f"  - Found {len(frame_files)} frame files")

    first_frame_path = os.path.join(frames_dir, frame_files[0])
    try:
        first_frame = cv2.imread(first_frame_path, cv2.IMREAD_COLOR)
        if first_frame is None:
            print(f"❌ Could not read frame: {first_frame_path}")
            return
    except Exception as e:
        print(f"❌ Error reading first frame: {str(e)}")
        print("💡 Try closing other applications to free up memory")
        return
        
    height, width, _ = first_frame.shape
    
    # Free up memory from first_frame
    del first_frame
    gc.collect()
    
    print(f"\n🎥 Video Properties:")
    print(f"  - Resolution: {width}x{height}")
    print(f"  - FPS: {fps:.2f}")
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
        
        try:
            frame_path = os.path.join(frames_dir, frame_files[frame_idx])
            frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)
            
            if frame is None:
                print(f"⚠️ Could not read frame {frame_path}. Skipping...")
                continue
                
            out.write(frame)
            
            # Free memory for the frame
            del frame
            
            # Periodic garbage collection
            if (i + 1) % 50 == 0:
                gc.collect()
            
        except Exception as e:
            print(f"⚠️ Error processing frame {frame_idx}: {str(e)}")
            continue
        
        # Show progress
        if (i + 1) % 50 == 0 or (i + 1) == len(order):
            print(f"  - Processed {i + 1}/{len(order)} frames...")

    out.release()
    

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

import os
import cv2
import numpy as np
from tqdm import tqdm
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import gc

def extract_features(frames_dir, output_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model = models.resnet18(pretrained=True)
    model = torch.nn.Sequential(*list(model.children())[:-1])  # remove classification layer
    model.to(device)
    model.eval()

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    features = []
    frame_files = sorted(os.listdir(frames_dir))
    
    print(f"Processing {len(frame_files)} frames...")
    
    # Process frames in batches to manage memory
    batch_size = 50
    failed_frames = []

    for i, f in enumerate(tqdm(frame_files, desc="Extracting features")):
        try:
            path = os.path.join(frames_dir, f)
            
            # Read image with error handling
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"\n⚠️ Warning: Could not read frame {f}, skipping...")
                failed_frames.append(f)
                continue
            
            # Resize image before processing to reduce memory
            if img.shape[0] > 1080 or img.shape[1] > 1920:
                img = cv2.resize(img, (1920, 1080))
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            tensor = transform(img).unsqueeze(0).to(device)
            
            with torch.no_grad():
                feat = model(tensor).cpu().numpy().flatten()
            features.append(feat)
            
            # Clean up memory every batch_size frames
            if (i + 1) % batch_size == 0:
                gc.collect()
                if device.type == 'cuda':
                    torch.cuda.empty_cache()
                    
        except Exception as e:
            print(f"\n❌ Error processing frame {f}: {str(e)}")
            failed_frames.append(f)
            continue

    if failed_frames:
        print(f"\n⚠️ Failed to process {len(failed_frames)} frames")
    
    if len(features) == 0:
        raise RuntimeError("No features extracted! All frames failed to process.")
    
    features = np.array(features)
    np.save(output_path, features)
    print(f"✅ Saved {len(features)} feature vectors to {output_path}")

if __name__ == "__main__":
    import os
    # Use relative paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frames_dir = os.path.join(base_dir, 'data', 'frames_jumbled')
    output_path = os.path.join(base_dir, 'data', 'frame_features.npy')
    
    print(f"Extracting features from: {frames_dir}")
    print(f"Saving features to: {output_path}")
    
    extract_features(frames_dir, output_path)

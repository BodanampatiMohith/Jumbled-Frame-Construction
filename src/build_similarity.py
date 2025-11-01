import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

def build_similarity():
    # Get the base directory (one level up from src)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define file paths
    features_path = os.path.join(base_dir, 'data', 'frame_features.npy')
    output_path = os.path.join(base_dir, 'data', 'similarity_matrix.npy')
    
    # Check if feature file exists
    if not os.path.exists(features_path):
        print("❌ Feature file not found. Run feature_extraction.py first.")
        return

    print(f"Loading features from: {features_path}")
    features = np.load(features_path)
    print(f"✅ Loaded features with shape: {features.shape}")

    # Compute similarity matrix
    print("🧠 Computing cosine similarity between frames...")
    similarity_matrix = cosine_similarity(features)
    
    # Save the similarity matrix
    np.save(output_path, similarity_matrix)
    print(f"✅ Saved similarity matrix to {output_path}")
    print(f"Matrix shape: {similarity_matrix.shape}")
    print(f"Similarity scores range: {np.min(similarity_matrix):.2f} to {np.max(similarity_matrix):.2f}")

if __name__ == "__main__":
    build_similarity()

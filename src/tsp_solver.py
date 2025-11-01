import numpy as np
import os

def tsp_reorder(similarity):
    """
    Reorder frames using a greedy TSP approach.
    
    Args:
        similarity: NxN similarity matrix where higher values indicate more similar frames
        
    Returns:
        list: Ordered list of frame indices
    """
    n = similarity.shape[0]
    visited = np.zeros(n, dtype=bool)
    order = [0]  # start from first frame
    visited[0] = True

    print(f"🔍 Finding optimal path through {n} frames...")
    
    for _ in range(n - 1):
        last = order[-1]
        sims = similarity[last].copy()  # Create a copy to avoid modifying original
        sims[visited] = -1  # Mark visited frames with -1 to avoid revisiting
        next_idx = np.argmax(sims)
        order.append(next_idx)
        visited[next_idx] = True
        
        # Show progress
        if (len(order) % 50) == 0:
            print(f"  - Processed {len(order)}/{n} frames...")

    return order

def solve_tsp():
    # Get the base directory (one level up from src)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define file paths
    sim_path = os.path.join(base_dir, 'data', 'similarity_matrix.npy')
    order_out = os.path.join(base_dir, 'data', 'frame_order_final.npy')
    
    # Check if similarity matrix exists
    if not os.path.exists(sim_path):
        print("❌ Similarity matrix not found. Run build_similarity.py first.")
        return

    print(f"🧩 Loading similarity matrix from: {sim_path}")
    similarity = np.load(sim_path)
    print(f"  - Matrix shape: {similarity.shape}")
    print(f"  - Similarity range: {np.min(similarity):.2f} to {np.max(similarity):.2f}")

    print("\n🚀 Solving frame order using greedy TSP approach...")
    order = tsp_reorder(similarity)
    
    # Calculate statistics
    forward_similarities = [similarity[order[i], order[i+1]] 
                          for i in range(len(order)-1)]
    
    print("\n📊 Reconstruction Statistics:")
    print(f"  - Number of frames: {len(order)}")
    print(f"  - Mean frame similarity: {np.mean(forward_similarities):.4f}")
    print(f"  - Min frame similarity: {np.min(forward_similarities):.4f}")
    print(f"  - Max frame similarity: {np.max(forward_similarities):.4f}")
    
    # Save the order
    np.save(order_out, np.array(order))
    print(f"\n✅ Frame order saved to: {order_out}")

if __name__ == "__main__":
    solve_tsp()

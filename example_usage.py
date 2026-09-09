"""Example usage for KD-Tree Spatial Indexer Skill."""
from client import KDTree2D

def main():
    print("Executing KD-Tree Spatial Indexer...")
    agents = [
        ((2.0, 3.0), "drone_alpha"),
        ((5.0, 4.0), "drone_bravo"),
        ((9.0, 6.0), "drone_charlie"),
        ((4.0, 7.0), "drone_delta")
    ]
    tree = KDTree2D(agents)
    target = (5.1, 4.1)
    pt, data, dist = tree.nearest_neighbor(target)
    print(f"Nearest agent to {target}: {data} at {pt} (dist={dist})")
    assert data == "drone_bravo", f"Expected drone_bravo, got {data}"
    print("KD-Tree Spatial Indexer verified successfully!")

if __name__ == "__main__":
    main()

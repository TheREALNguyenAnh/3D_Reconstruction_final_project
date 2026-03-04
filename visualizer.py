import sys
import open3d as o3d

# load and visualize point cloud from a ply file
# ply_path - Path to the input point cloud file (.ply).
def load_points(ply_path):
    try:
        print(f"Loading point cloud from '{ply_path}'...")
        pcd = o3d.io.read_point_cloud(ply_path) # Load point cloud from specified ply file

        print("Displaying point cloud...")
        o3d.visualization.draw_geometries([pcd]) # Visualize point cloud
    except Exception as e:
        print("Error: failed to load point cloud or file is empty.")
        sys.exit(1)

# test function to verify that the visualizer can load and display a point cloud
def test():
    print("Running visualizer test...")
    load_points("test.ply")
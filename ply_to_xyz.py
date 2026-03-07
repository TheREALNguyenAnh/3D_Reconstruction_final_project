import sys
import open3d as o3d
import numpy as np

def convert_ply_to_xyz(ply_path, xyz_path=None, include_colors=True):
    
    if xyz_path is None:
        xyz_path = ply_path.rsplit('.', 1)[0] + '.xyz'
    
    print(f"Loading {ply_path}...")
    pcd = o3d.io.read_point_cloud(ply_path)
    
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors) if pcd.has_colors() and include_colors else None
    
    print(f"Writing {len(points)} points to {xyz_path}...")
    
    with open(xyz_path, 'w') as f:
        for i in range(len(points)):
            x, y, z = points[i]
            if colors is not None:
                r, g, b = (colors[i] * 255).astype(int)
                f.write(f"{x} {y} {z} {r} {g} {b}\n")
            else:
                f.write(f"{x} {y} {z}\n")
    
    print(f"Done! Saved to {xyz_path}")

if __name__ == "__main__":
    ply_path = sys.argv[1]
    xyz_path = sys.argv[2] if len(sys.argv) > 2 else None
    convert_ply_to_xyz(ply_path, xyz_path)

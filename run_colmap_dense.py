import os
import pycolmap

# Paths - change these as needed
IMAGE_DIR = "test_dir"
WORKSPACE = "colmap_workspace"


def run_dense_reconstruction():
    """Run MVS dense reconstruction using native PyColmap functions.
    
    Requires sparse reconstruction to be completed first.
    Run either run_colmap_sparse_sequential.py or run_colmap_sparse_exhaustive.py first.
    """
    workspace = os.path.abspath(WORKSPACE)
    image_dir = os.path.abspath(IMAGE_DIR)
    sparse_dir = os.path.join(workspace, "sparse", "0")
    dense_dir = os.path.join(workspace, "dense")
    
    # Check sparse reconstruction exists
    if not os.path.exists(sparse_dir):
        print("Error: Sparse reconstruction not found at", sparse_dir)
        print("Run sparse reconstruction first:")
        print("  python run_colmap_sparse_sequential.py")
        print("  or")
        print("  python run_colmap_sparse_exhaustive.py")
        return False
    
    os.makedirs(dense_dir, exist_ok=True)
    
    print("=" * 50)
    print("DENSE RECONSTRUCTION (MVS)")
    print("=" * 50)
    
    # GPU check for patch match (requires CUDA)
    if not pycolmap.has_cuda:
        print("Error: Dense reconstruction requires CUDA GPU.")
        return False
    
    # 1. Image Undistortion
    print("\nStep 1/3: Image Undistortion")
    pycolmap.undistort_images(
        output_path=dense_dir,
        input_path=sparse_dir,
        image_path=image_dir,
        output_type="COLMAP"
    )
    print("Undistortion complete.")
    
    # 2. Patch Match Stereo (GPU depth estimation)
    print("\nStep 2/3: Patch Match Stereo (computing depth maps...)")
    print("This may take a while depending on image count and resolution.")
    
    pm_options = pycolmap.PatchMatchOptions()
    pm_options.geom_consistency = True
    
    pycolmap.patch_match_stereo(
        workspace_path=dense_dir,
        workspace_format="COLMAP",
        options=pm_options
    )
    print("Depth map computation complete.")
    
    # 3. Stereo Fusion
    print("\nStep 3/3: Stereo Fusion")
    dense_ply_path = os.path.join(dense_dir, "fused.ply")
    
    fusion_options = pycolmap.StereoFusionOptions()
    
    dense_model = pycolmap.stereo_fusion(
        output_path=dense_ply_path,
        workspace_path=dense_dir,
        workspace_format="COLMAP",
        input_type="geometric",
        options=fusion_options
    )
    
    print(f"\nDense reconstruction complete!")
    print(f"Dense point cloud: {dense_ply_path}")
    print(f"Total 3D Points (dense): {len(dense_model.points3D):,}")
    
    return True


if __name__ == "__main__":
    run_dense_reconstruction()

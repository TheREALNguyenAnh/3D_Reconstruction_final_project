import os
import pycolmap

# Paths - change these as needed
IMAGE_DIR = "test_dir"
WORKSPACE = "colmap_workspace"


def run_sparse_reconstruction():
    """Run feature extraction, matching, and sparse reconstruction."""
    workspace = os.path.abspath(WORKSPACE)
    image_dir = os.path.abspath(IMAGE_DIR)
    database_path = os.path.join(workspace, "database.db")
    sparse_dir = os.path.join(workspace, "sparse")
    
    os.makedirs(workspace, exist_ok=True)
    os.makedirs(sparse_dir, exist_ok=True)
    
    # Verify GPU Status
    if pycolmap.has_cuda:
        print("--- GPU DETECTED ---")
        dev = pycolmap.Device.cuda
    else:
        print("--- GPU NOT DETECTED (FALLING BACK TO CPU) ---")
        dev = pycolmap.Device.cpu

    # 1. Feature Extraction
    print("\nStep 1/3: Feature Extraction")
    pycolmap.extract_features(
        database_path=database_path,
        image_path=image_dir,
        camera_mode=pycolmap.CameraMode.SINGLE,
        extraction_options=pycolmap.FeatureExtractionOptions(),
        device=dev
    )
    
    # 2. Exhaustive Matching
    print("\nStep 2/3: Exhaustive Matching")
    pycolmap.match_exhaustive(
        database_path=database_path,
        matching_options=pycolmap.FeatureMatchingOptions(),
        device=dev
    )
    
    # 3. Sparse Reconstruction (Mapper)
    print("\nStep 3/3: Sparse Reconstruction")
    maps = pycolmap.incremental_mapping(
        database_path=database_path,
        image_path=image_dir,
        output_path=sparse_dir
    )
    
    if maps:
        print(f"\nSparse reconstruction complete! {len(maps)} model(s) created.")
        model = maps[0]
        model.write(sparse_dir)
        model.export_PLY(os.path.join(sparse_dir, "sparse.ply"))
        print(f"Sparse point cloud: {sparse_dir}/sparse.ply")
        print(f"Total 3D Points (sparse): {len(model.points3D)}")
        return True
    else:
        print("\nMapping failed. Try increasing image overlap or quality.")
        return False


def run_dense_reconstruction():
    """Run MVS dense reconstruction using native PyColmap functions."""
    workspace = os.path.abspath(WORKSPACE)
    image_dir = os.path.abspath(IMAGE_DIR)
    sparse_dir = os.path.join(workspace, "sparse", "0")
    dense_dir = os.path.join(workspace, "dense")
    
    # Check sparse reconstruction exists
    if not os.path.exists(sparse_dir):
        print("Error: Sparse reconstruction not found at", sparse_dir)
        print("Run sparse reconstruction first: python run_colmap.py --sparse-only")
        return False
    
    os.makedirs(dense_dir, exist_ok=True)
    
    print("\n" + "=" * 50)
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


def run_full_pipeline():
    """Run complete reconstruction pipeline (sparse + dense)."""
    print("=" * 50)
    print("FULL 3D RECONSTRUCTION PIPELINE")
    print("=" * 50)
    
    if not run_sparse_reconstruction():
        return
    
    run_dense_reconstruction()


if __name__ == "__main__":
    run_full_pipeline()
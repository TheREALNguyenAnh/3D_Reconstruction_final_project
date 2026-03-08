import os
import pycolmap

# Paths - change these as needed
IMAGE_DIR = "test_dir"
WORKSPACE = "colmap_workspace"


def run_sparse_reconstruction():
    """Run feature extraction, sequential matching, and sparse reconstruction."""
    workspace = os.path.abspath(WORKSPACE)
    image_dir = os.path.abspath(IMAGE_DIR)
    database_path = os.path.join(workspace, "database.db")
    sparse_dir = os.path.join(workspace, "sparse")
    
    os.makedirs(workspace, exist_ok=True)
    os.makedirs(sparse_dir, exist_ok=True)
    
    print("=" * 50)
    print("SPARSE RECONSTRUCTION (SEQUENTIAL MATCHING)")
    print("=" * 50)
    
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
    
    # 2. Sequential Matching
    print("\nStep 2/3: Sequential Matching")
    pycolmap.match_sequential(
        database_path=database_path,
        matching_options=pycolmap.FeatureMatchingOptions(),
        pairing_options=pycolmap.SequentialPairingOptions(overlap=10),
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


if __name__ == "__main__":
    run_sparse_reconstruction()

import os
import pycolmap

# Paths - change these as needed
IMAGE_DIR = "test_dir"
WORKSPACE = "colmap_workspace"

def runColmap():
    workspace = os.path.abspath(WORKSPACE)
    image_dir = os.path.abspath(IMAGE_DIR)
    database_path = os.path.join(workspace, "database.db")
    sparse_dir = os.path.join(workspace, "sparse")
    
    os.makedirs(workspace, exist_ok=True)
    os.makedirs(sparse_dir, exist_ok=True)
    
    # Verify GPU Status
    if pycolmap.has_cuda:
        print("--- GPU (RTX 4060) DETECTED ---")
        dev = pycolmap.Device.cuda
    else:
        print("--- GPU NOT DETECTED (FALLING BACK TO CPU) ---")
        dev = pycolmap.Device.cpu

    # 1. Feature Extraction
    print("\nRunning: Feature Extraction")
    # In 3.13+, we use FeatureExtractionOptions instead of SiftExtractionOptions
    pycolmap.extract_features(
        database_path=database_path,
        image_path=image_dir,
        camera_mode=pycolmap.CameraMode.SINGLE,
        extraction_options=pycolmap.FeatureExtractionOptions(), # <--- Correct Class
        device=dev
    )
    
    # 2. Sequential Matching
    print("\nRunning: Sequential Matching")
    # In 3.13+, keyword names have shifted to matching_options and pairing_options
    pycolmap.match_sequential(
        database_path=database_path,
        matching_options=pycolmap.FeatureMatchingOptions(),      # <--- New Keyword/Class
        pairing_options=pycolmap.SequentialPairingOptions(overlap=10), # <--- New Keyword
        device=dev
    )
    
    # 3. Sparse Reconstruction (Mapper)
    print("\nRunning: Sparse Reconstruction")
    maps = pycolmap.incremental_mapping(
        database_path=database_path,
        image_path=image_dir,
        output_path=sparse_dir
    )
    
    if maps:
        print(f"\nSuccess! {len(maps)} model(s) created.")
        # Save results for Open3D/Meshlab
        model = maps[0]
        model.write(sparse_dir)
        # Export as a standard 3D file for your report
        model.export_PLY(os.path.join(sparse_dir, "reconstruction.ply"))
        print(f"Point cloud exported to: {sparse_dir}/reconstruction.ply")
        print(f"Total 3D Points: {len(model.points3D)}")
    else:
        print("\nMapping failed to produce a model. Try increasing image overlap.")

if __name__ == "__main__":
    runColmap()
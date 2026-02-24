# 3D Reconstruction Final Project

> Final project for Computational Photography class

---

## Installation

### Required Packages

```bash
pip install opencv-python open3d
```

### COLMAP

```bash
# Ubuntu/Debian
sudo apt-get install colmap

# Or build from source: https://colmap.github.io/install.html
```

### Optional

```bash
# For AI background removal (only if needed)
pip install rembg
```

---

## Phase 0: Data Collection

- Film video of a specular non-transparent object
- Use sunlight; preferably avoid shadows if possible
- Obtain a sample video or dataset that is confirmed to be good enough for reconstruction

---

## Phase 1: Data Engineering (Input Handling)

**Target:** Turn a video file into a clean folder of images.

### 1.1 Frame Extraction Script
- [ ] Write `video_processor.py`
- **Input:** `.mp4` path
- **Logic:** Use OpenCV to save every few frames to an `images/` folder

### 1.2 Blur Detection Filter
- [ ] Update `video_processor.py`
- **Logic:** Calculate Laplacian Variance for each frame. If variance < threshold (blurry), discard it.

### 1.3 [OPTIONAL] AI Background Removal
- [ ] Write `mask_generator.py`
- **Logic:** Use `rembg` library to generate binary masks. Save to `masks/` folder.

- **Note:** Backgrounds actually HELP feature matching. Only use this if the reconstruction fails due to moving background objects.

---

## Phase 2: Structure Engine (COLMAP Automation)

**Target:** Get a sparse point cloud (dots) from the images.

### 2.1 Manual Test
- [ ] Install COLMAP
- [ ] Run the GUI manually on a sample dataset to ensure it works on your machine

### 2.2 Feature Extraction Script
- [ ] Write `run_colmap.py` (Part 1)
- **Logic:** Use `subprocess` to call `colmap feature_extractor`
  - Point it directly to the `images/` folder
  - Only pass the mask path if Task 1.3 was needed

### 2.3 Matcher Script
- [ ] Update `run_colmap.py` (Part 2)
- **Logic:** Call `colmap exhaustive_matcher` (or `sequential_matcher` if video frames are ordered)

### 2.4 Sparse Reconstruction Script
- [ ] Update `run_colmap.py` (Part 3)
- **Logic:** Call `colmap mapper`
  - Generates the camera poses and sparse points

### 2.5 Export Data
- [ ] Write `export_data.py`
- **Logic:** Convert COLMAP's `.bin` output to `.ply` (Point Cloud) using `colmap model_converter`

---

## Phase 3: Densification & Baseline Meshing

**Target:** Turn the dots into a solid, vertex-colored object (The Baseline).

### 3.1 Visualizer
- [ ] Write `visualizer.py`
- **Logic:** Use `open3d.io.read_point_cloud` to load the `.ply` file and display it

### 3.2 Dense Reconstruction (MVS)
- [ ] Update `run_colmap.py` (Part 4)
- **Logic:** Run the following commands:
  - `colmap image_undistorter`
  - `colmap patch_match_stereo`
  - `colmap stereo_fusion`
- **Result:** A high-density, colored `.ply` file (millions of points)

### 3.3 Statistical Outlier Removal
- [ ] Write `mesher.py` (Part 1)
- **Logic:** Load dense cloud in Open3D. Use `remove_statistical_outlier` to delete floating noise points.

### 3.4 Poisson Surface Reconstruction (Vertex-Colored Mesh)
- [ ] Update `mesher.py` (Part 2)
- **Logic:**
  - Run `o3d.geometry.TriangleMesh.create_from_point_cloud_poisson`
  - Project the colors from the dense point cloud onto the new mesh vertices
- **Result:** A solid `.obj` mesh with colors baked into the vertices (Baseline complete!)
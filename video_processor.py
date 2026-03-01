import os
import cv2

#Extract frames from a video file at a given interval and save them as images.
#video_path - Path to the input video (.mp4).
#output_dir - Directory where extracted images will be saved.
#interval - Number of frames between each saved image (default: 24).
def extract_frames(video_path, output_dir, interval = 24):
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video: {video_path}")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            filename = os.path.join(output_dir, f"frame_{saved_count:06d}.png")
            cv2.imwrite(filename, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted {saved_count} frames from {video_path} to {output_dir}")

#method for testing
def test():
    video_path = "test.mp4"
    output_dir = "test_dir"
    extract_frames(video_path, output_dir)


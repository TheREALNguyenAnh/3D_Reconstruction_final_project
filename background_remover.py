import os
from rembg import remove
from PIL import Image

def remove_background_single(input_path, output_path):
    # Load the image
    input_image = Image.open(input_path)

    # Remove background
    output = remove(input_image)

    # Save result
    output.save(output_path)

    print(f"Background removed and saved to {output_path}")

def batch_remove_background(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.split(".")[0] + "_no_bg.png")

            with Image.open(input_path) as img:
                output = remove(img)
                output.save(output_path)

            print(f"Processed: {filename}")


batch_remove_background("testLap", "output")
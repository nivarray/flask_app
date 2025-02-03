from PIL import Image
import glob
import os

# Define directory paths
full_path = "app/static/annotation_and_img"
output_dir = "cropped_pollen"

# Loop through all JPG images in the directory
for img_file in glob.glob(os.path.join(full_path, "*.jpg")):
    # Open the image
    img = Image.open(img_file)

    # Extract image name without extension
    img_name = os.path.splitext(os.path.basename(img_file))[0]

    # Find corresponding annotation file
    ann_file = os.path.join(full_path, f"{img_name}.txt")
    if not os.path.exists(ann_file):
        print(f"Warning: No annotation file for {img_file}, skipping...")
        continue  # Skip if no matching annotation file

    # Read annotation file
    annotation_lines = []
    with open(ann_file, "r") as file:
        for line in file:
            annotation_lines.append(line.split())

    # Get image dimensions
    image_width, image_height = img.size

    # Process each annotation
    for i, ann in enumerate(annotation_lines):
        pollen_id = ann[0]
        xmid, ymid, box_width, box_height = map(float, ann[1:])

        # Convert YOLO format to pixel coordinates
        x_mid_px = xmid * image_width
        y_mid_px = ymid * image_height
        box_width_px = box_width * image_width
        box_height_px = box_height * image_height

        x_min = int(x_mid_px - box_width_px / 2)
        y_min = int(y_mid_px - box_height_px / 2)
        x_max = int(x_mid_px + box_width_px / 2)
        y_max = int(y_mid_px + box_height_px / 2)

        # Crop the bounding box
        cropped_img = img.crop((x_min, y_min, x_max, y_max))

        # Create pollen-specific output directory
        pollen_dir = os.path.join(output_dir, pollen_id)
        os.makedirs(pollen_dir, exist_ok=True)

        # Save cropped image with correct filename
        crop_filename = f"{i}_cropped_from_{img_name}.jpg"
        cropped_img.save(os.path.join(pollen_dir, crop_filename))

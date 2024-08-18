from PIL import Image, ImageEnhance
import os
import random

def apply_overlay_with_opacity(image, overlay, opacity=0.5):
    # Resize the overlay to match the image size
    overlay = overlay.resize(image.size)

    # Decrease the opacity of the overlay
    overlay = overlay.copy()
    alpha = overlay.split()[3]  # Get the alpha channel
    alpha = alpha.point(lambda p: p * opacity)  # Apply the opacity to the alpha channel
    overlay.putalpha(alpha)

    # Blend the overlay on top of the original image
    image_with_overlay = Image.alpha_composite(image, overlay)

    # Optionally, reduce the color saturation and brightness
    image_with_overlay = ImageEnhance.Color(image_with_overlay).enhance(random.uniform(0.6, 0.9))
    image_with_overlay = ImageEnhance.Brightness(image_with_overlay).enhance(random.uniform(0.8, 0.9))

    return image_with_overlay.convert("RGB")

def apply_overlay_to_images(image_folder, overlay_folder, output_folder, opacity=0.5):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get list of all image files in the folder
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))])

    # Get list of all overlay files in the folder
    overlay_files = sorted([f for f in os.listdir(overlay_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))])

    # Apply a random overlay to each image
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        image = Image.open(image_path).convert("RGBA")

        # Randomly select an overlay
        overlay_file = random.choice(overlay_files)
        overlay_path = os.path.join(overlay_folder, overlay_file)
        overlay = Image.open(overlay_path).convert("RGBA")

        # Apply the overlay to the image
        image_with_overlay = apply_overlay_with_opacity(image, overlay, opacity)

        # Rename the output file by changing the prefix
        output_filename = f"T{os.path.splitext(image_file)[0][1:]}.png"
        output_path = os.path.join(output_folder, output_filename)

        # Save the processed image
        image_with_overlay.save(output_path)

        print(f"Processed {image_file} with random overlay {overlay_file} and saved to {output_path}")

# Example usage
image_folder = 'Dataset/restored'
overlay_folder = 'overlay'
output_folder = 'dataset/scratches'

apply_overlay_to_images(image_folder, overlay_folder, output_folder, opacity=0.5)

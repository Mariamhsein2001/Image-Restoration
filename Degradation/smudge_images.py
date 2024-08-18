import cv2 # type: ignore
import os
import random
import numpy as np
from PIL import Image

def apply_random_smudge(image, smudge_folder):
    # Load all smudge images from the folder
    smudge_images = [os.path.join(smudge_folder, f) for f in os.listdir(smudge_folder)]
    
    # Randomly select a smudge image
    smudge_path = random.choice(smudge_images)
    smudge = Image.open(smudge_path).convert("RGBA")
    
    # Convert the target image to RGBA if it isn't already
    image = Image.fromarray(image).convert("RGBA")

    # Ensure the smudge is smaller than the image
    img_width, img_height = image.size
    if smudge.width > img_width or smudge.height > img_height:
        scale = min(img_width / smudge.width, img_height / smudge.height) * 0.9
        smudge = smudge.resize((int(smudge.width * scale), int(smudge.height * scale)), Image.LANCZOS)
    else:
        # Randomly resize smudge if already smaller
        scale = random.uniform(0.3, 1.0)
        smudge = smudge.resize((int(smudge.width * scale), int(smudge.height * scale)), Image.LANCZOS)
    
    # Get dimensions for placing the smudge
    smudge_width, smudge_height = smudge.size

    # Random position for smudge
    x_offset = random.randint(0, img_width - smudge_width)
    y_offset = random.randint(0, img_height - smudge_height)
    
    # Place smudge on image
    image.paste(smudge, (x_offset, y_offset), smudge)

    return np.array(image)


# Example usage:
input_folder = r'C:\Users\Hp\Desktop\RestoredImages\Images'
output_folder = r'C:\Users\Hp\Desktop\SmudgedImages\Images'
smudge_folder = r'G:\My Drive\degradation\smudges'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        
        # Apply random smudge to the image
        image_with_smudge = apply_random_smudge(image, smudge_folder)
        print("image smudged successfully")
        
        # Generate the corresponding output filename
        base_filename = os.path.splitext(filename)[0]  # Get the base name without extension
        smudged_filename = base_filename.replace('R', 'S') + '.png'  # Replace 'R' with 'S' and add .png extension
        
        # Save the resulting image
        output_path = os.path.join(output_folder, smudged_filename)
        cv2.imwrite(output_path, image_with_smudge)

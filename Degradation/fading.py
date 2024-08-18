import os
import random
from PIL import Image, ImageDraw, ImageFilter

def create_realistic_gradient_mask(image_size, direction, fade_amount):
    width, height = image_size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    if direction == 'left':
        for x in range(width):
            fill_value = int(255 * (x / width) * fade_amount)
            draw.line([(x, 0), (x, height)], fill=fill_value)
    elif direction == 'right':
        for x in range(width):
            fill_value = int(255 * ((width - x) / width) * fade_amount)
            draw.line([(x, 0), (x, height)], fill=fill_value)
    elif direction == 'top':
        for y in range(height):
            fill_value = int(255 * (y / height) * fade_amount)
            draw.line([(0, y), (width, y)], fill=fill_value)
    elif direction == 'bottom':
        for y in range(height):
            fill_value = int(255 * ((height - y) / height) * fade_amount)
            draw.line([(0, y), (width, y)], fill=fill_value)
    elif direction == 'middle':
        for y in range(height):
            for x in range(width):
                fade_x = abs(x - width // 2) / (width // 2)
                fade_y = abs(y - height // 2) / (height // 2)
                fill_value = int(255 * max(fade_x, fade_y) * fade_amount)
                mask.putpixel((x, y), fill_value)

    # Add random noise for more natural fading
    noise = Image.effect_noise(image_size, random.uniform(5, 15))
    mask = Image.blend(mask, noise, 0.2)  # Blend with a small amount of noise

    # Blur the mask for smoother transitions
    mask = mask.filter(ImageFilter.GaussianBlur(radius=random.uniform(2, 5)))

    return mask

def apply_fade(image, direction='left', fade_amount=0.5):
    # Convert the image to RGBA (to have an alpha channel)
    image = image.convert('RGBA')
    width, height = image.size

    # Create a gradient mask
    mask = create_realistic_gradient_mask(image.size, direction, fade_amount)

    # Create an image with the fade color (white)
    fade_color = (255, 255, 255, 255)
    fade_image = Image.new('RGBA', (width, height), fade_color)

    # Apply the mask to the fade image
    faded_image = Image.composite(fade_image, image, mask)

    return faded_image.convert('RGB') if image.mode == 'RGB' else faded_image.convert('RGBA')

def process_images(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    for i, image_file in enumerate(image_files):
        # Load the image
        image_path = os.path.join(input_folder, image_file)
        image = Image.open(image_path)

        # Randomly select a fading direction and amount
        direction = random.choice(['left', 'right', 'top', 'bottom', 'middle'])
        fade_amount = random.uniform(0.4, 0.9)  # Random fade amount between 0.4 and 0.9

        # Apply fading effect
        faded_image = apply_fade(image, direction=direction, fade_amount=fade_amount)

        # Modify the file name by removing 'R' and prefixing with 'F'
        base_name, extension = os.path.splitext(image_file)
        if base_name.startswith('R'):
            base_name = base_name[1:]
        output_filename = f"F{base_name}.png"

        # Save the faded image with the new name
        output_path = os.path.join(output_folder, output_filename)
        faded_image.save(output_path)
        print(f"Processed {image_file} with fade direction '{direction}' and saved as {output_path}")

# Example usage:
input_folder = r"C:\Users\user\Desktop\Restorating-Images\Dataset\restored"
output_folder = r"C:\Users\user\Desktop\Restorating-Images\Dataset\faded"

process_images(input_folder, output_folder)

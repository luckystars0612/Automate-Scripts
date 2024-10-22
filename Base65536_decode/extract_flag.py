from PIL import Image
import numpy as np

# Load the image
image_path = 'download.png'
img = Image.open(image_path)

# Convert image to numpy array
pixels = np.array(img)

# List to hold unique RGB values while preserving order
unique_rgb = []
seen = set()

# Iterate over every pixel row by row
for row in pixels:
    for pixel in row:
        # Convert the pixel to a tuple to make it hashable (for comparison)
        pixel_tuple = tuple(pixel[:3])  # Only consider RGB, ignore alpha if present

        # Filter out white pixels (255, 255, 255) and keep only unique ones
        if pixel_tuple != (255, 255, 255) and pixel_tuple not in seen:
            unique_rgb.append(pixel_tuple)
            seen.add(pixel_tuple)

# Concatenate the RGB values into a single string (in hex format)
rgb_string = ''.join([f'{r:02x}{g:02x}{b:02x}' for r, g, b in unique_rgb])

# Attempt to decode the hex string as UTF-8
try:
    decoded_string = bytes.fromhex(rgb_string).decode('utf-8')
    print("Decoded UTF-8 string:", decoded_string)
except UnicodeDecodeError:
    print("Failed to decode the concatenated string as UTF-8")

# Optional: Write the RGB hex string to a file
with open('output_rgb_hex.txt', 'w') as f:
    f.write(rgb_string)

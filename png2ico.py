from PIL import Image
import os

# Load the image
img_path = 'icon.png'
img = Image.open(img_path)

# The ICO format supports multiple sizes, so here we'll define a list of desired sizes.
ico_sizes = [(256, 256)]

# Convert the image and save as .ico file
output_path = 'icon.ico'
img.save(output_path, format='ICO', sizes=ico_sizes)

output_path

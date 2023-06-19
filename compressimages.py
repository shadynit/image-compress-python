import os
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True  # Handle truncated images

size = (1000, 1000)
source_dir = '/source' # Source Directory
dest_dir = '/destination' # Destination Directory
fill_color = '#ffffff'
max_pixels = 178956970  # Maximum allowed number of pixels

try:
    os.makedirs(dest_dir)
except OSError:
    pass  # Directory already exists

for infile in os.listdir(source_dir):
    if os.path.splitext(infile)[1].lower() in ('.jpg', '.jpeg', '.png'):
        file, ext = os.path.splitext(infile)
        image_path = os.path.join(source_dir, infile)
        
        try:
            image = Image.open(image_path)
            if image.mode in ('RGBA', 'LA'):
                background = Image.new(image.mode[:-1], image.size, fill_color)
                background.paste(image, image.split()[-1])
                image = background

            # Check if image exceeds the maximum allowed size
            if image.size[0] * image.size[1] > max_pixels:
                image.thumbnail(size)
                print(f'Skipping {file} due to size limit exceeded')
                continue  # Skip the file and proceed to the next iteration

            image = image.resize(size)
            image.save(os.path.join(dest_dir, file + '.jpg'), "JPEG", optimize=True, quality=100)
            print('Compressing', file)
            
        except Image.DecompressionBombError:
            print(f'Skipping {file} due to decompression bomb DOS attack potential')
            continue  # Skip the file and proceed to the next iteration

print("Job Completed!")

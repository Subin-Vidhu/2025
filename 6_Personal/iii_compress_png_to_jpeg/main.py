import os
from PIL import Image

def compress_to_jpeg(input_path, output_path, target_size=2 * 1024 * 1024):
    quality = 95  # start high, reduce if needed

    with Image.open(input_path) as img:
        # Remove alpha if it exists
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # paste using alpha channel as mask
            img = background
        else:
            img = img.convert('RGB')

        # Try different quality levels until under target_size
        while quality > 10:
            img.save(output_path, 'JPEG', quality=quality)
            if os.path.getsize(output_path) <= target_size:
                break
            quality -= 5  # reduce quality

        final_size = os.path.getsize(output_path)
        if final_size <= target_size:
            print(f"✅ {os.path.basename(input_path)} compressed to {final_size / (1024 * 1024):.2f} MB (quality={quality})")
        else:
            print(f"⚠️ {os.path.basename(input_path)} still above 2MB even at quality={quality}")

# Batch convert folder
input_folder = "C:\\Users\\ASUS\\OneDrive\\Pictures\\Scans\\SUBIN\\compress"
output_folder = "C:\\Users\\ASUS\\OneDrive\\Pictures\\Scans\\SUBIN\\jpeg_output"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.png'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpg')
        compress_to_jpeg(input_path, output_path)

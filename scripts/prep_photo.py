import os
import sys
import io
import requests
from PIL import Image, ImageEnhance, ImageOps

def download_avatar_if_needed(filename="source-photo.jpg", username="Prasadhol2001"):
    if not os.path.exists(filename):
        print(f"[{filename}] not found locally. Fetching profile photo from GitHub for '{username}'...")
        url = f"https://github.com/{username}.png"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200:
            with open(filename, "wb") as f:
                f.write(resp.content)
            print(f"Downloaded profile avatar to '{filename}' ({len(resp.content)} bytes).")
        else:
            raise RuntimeError(f"Failed to fetch avatar from {url}, HTTP status {resp.status_code}")

def prep_photo(input_path="source-photo.jpg", output_path="source-prepped.png", username="Prasadhol2001"):
    download_avatar_if_needed(input_path, username)
    
    print(f"Prepping photo: '{input_path}' -> '{output_path}'")
    img = Image.open(input_path).convert("RGBA")
    
    # 1. Composite onto pure white background
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, img).convert("L")
    
    # 2. Apply autocontrast & Local Contrast Enhancement via PIL
    enhanced = ImageOps.autocontrast(composite, cutoff=2)
    enhancer = ImageEnhance.Contrast(enhanced)
    final_img = enhancer.enhance(1.8)
    
    # 3. Brightness adjustment to ensure highlights map to empty space
    brightener = ImageEnhance.Brightness(final_img)
    final_img = brightener.enhance(1.1)
    
    final_img.save(output_path)
    print(f"Successfully saved prepped image to '{output_path}' ({final_img.size[0]}x{final_img.size[1]}px).")

if __name__ == "__main__":
    target_in = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    target_out = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    user = sys.argv[3] if len(sys.argv) > 3 else "Prasadhol2001"
    prep_photo(target_in, target_out, user)

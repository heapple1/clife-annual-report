import os, shutil
from PIL import Image
import numpy as np

MEMBERS_DIR = os.path.join(os.path.dirname(__file__), "media", "members")

def remove_green_bg(filepath):
    name = os.path.splitext(os.path.basename(filepath))[0]
    if name == "字体模板":
        return
    print(f"Processing: {name}")
    img = Image.open(filepath).convert("RGBA")
    arr = np.array(img).astype(float)
    
    # Green background: G channel much higher than R and B
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    # Pixel is "green" if G is dominant and G > threshold
    is_green = (g > 80) & (g > r + 20) & (g > b + 20)
    
    # Create alpha: non-green = opaque, green = transparent
    alpha = np.where(is_green, 0, 255).astype(np.uint8)
    
    img.putalpha(Image.fromarray(alpha, mode='L'))
    
    # Crop to content
    bbox = img.split()[3].getbbox()
    if bbox:
        pad = 5
        bbox = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(img.width, bbox[2] + pad),
            min(img.height, bbox[3] + pad)
        )
        img = img.crop(bbox)
    
    out_path = os.path.join(MEMBERS_DIR, name + ".png")
    img.save(out_path, "PNG")
    print(f"  Saved: {out_path} ({img.width}x{img.height})")

def main():
    # Clean old PNGs
    for f in os.listdir(MEMBERS_DIR):
        if f.endswith('.png'):
            os.remove(os.path.join(MEMBERS_DIR, f))
    
    # Copy new originals
    src_dir = r"D:\HuaweiMoveData\Users\贺靖茹\Desktop\C_Life\九周年庆\会员个人照"
    for f in os.listdir(src_dir):
        if f.endswith('.jpg') and f != '字体模板.jpg':
            shutil.copy(os.path.join(src_dir, f), os.path.join(MEMBERS_DIR, f))
    
    # Process each
    for f in os.listdir(MEMBERS_DIR):
        if f.endswith('.jpg') and f != '字体模板.jpg':
            filepath = os.path.join(MEMBERS_DIR, f)
            remove_green_bg(filepath)
            os.remove(filepath)
    
    print("All done!")

if __name__ == "__main__":
    main()

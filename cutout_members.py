import os
from PIL import Image, ImageFilter
import numpy as np

MEMBERS_DIR = os.path.join(os.path.dirname(__file__), "media", "members")

def remove_black_outside(filepath):
    """Only remove black background OUTSIDE the white border.
    Keep everything inside the border (person + white outline) untouched."""
    name = os.path.splitext(os.path.basename(filepath))[0]
    if name == "字体模板":
        return
    print(f"Processing: {name}")
    img = Image.open(filepath).convert("RGBA")
    arr = np.array(img).astype(float)
    
    # Detect black pixels: R, G, B all very low
    brightness = arr[:, :, :3].max(axis=2)
    
    # Only make truly black pixels transparent
    # Keep everything else (including gray shadows near border) unchanged
    alpha = np.where(brightness < 15, 0, 255).astype(np.uint8)
    
    # Apply new alpha
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
    # Re-copy originals first
    import shutil
    src_dir = r"D:\HuaweiMoveData\Users\贺靖茹\Desktop\C_Life\九周年庆\会员个人照"
    for f in os.listdir(src_dir):
        if f.endswith('.jpg'):
            shutil.copy2(os.path.join(src_dir, f), os.path.join(MEMBERS_DIR, f))
    
    # Process each
    for f in os.listdir(MEMBERS_DIR):
        if f.endswith('.jpg') and f != '字体模板.jpg':
            filepath = os.path.join(MEMBERS_DIR, f)
            remove_black_outside(filepath)
            os.remove(filepath)
    
    print("All done!")

if __name__ == "__main__":
    main()

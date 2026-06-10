#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Book-001 picture book pages V4.
Horizontal layout 1920x1080, reference Book-021 subtitle style.
Input: pages/*.png (raw scenes from user)
Output: pages_v4/*.png (with subtitles)
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont

# --- Config (Horizontal 1920x1080, reference Book-021) ---
SCRIPT_MD = "script.md"
INPUT_DIR = "pages"   # user's 13 raw images (resized to 1224x936)
OUTPUT_DIR = "pages_v4"
WIDTH, HEIGHT = 1920, 1080

# Layout: image area top 0~650, subtitle area bottom 650~1080
IMG_AREA_H = 650
IMG_Y = 0  # image top aligned

# Subtitle area: y=650~1080 (430px height)
SUB_EN_Y = [680, 730]       # English: 2 lines
SUB_EN2_Y = [780, 830]     # English 2: 2 lines  
SUB_CN_Y = [880, 930]       # Chinese: 2 lines
SUB_CN2_Y = [980, 1030]   # Chinese 2: 2 lines

# Font sizes (horizontal, larger than vertical)
FONT_SIZE_EN = 28
FONT_SIZE_EN2 = 24
FONT_SIZE_CN = 26
FONT_SIZE_CN2 = 22

# Colors
BG_COLOR = (250, 246, 240)   # #FAF6F0 warm beige
FONT_COLOR = (60, 40, 30)  # dark brown

def get_font(size, cn=False):
    """Load font with fallback."""
    if cn:
        paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
        ]
    else:
        paths = [
            "C:/Windows/Fonts/comic.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def wrap_text(text, font, max_width):
    """Wrap text to multiple lines. Max 2 lines."""
    if not text:
        return []
    lines = []
    words = text.split()
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines[:2]  # Max 2 lines!

def create_page(scene_idx, scene):
    """Create one page (1920x1080) from one raw image."""
    # Load raw image (user provided, already resized to 1224x936)
    in_path = os.path.join(INPUT_DIR, f"page{scene_idx:02d}.png")
    if not os.path.exists(in_path):
        print(f"  [WARN] Missing: {in_path}")
        return False
    
    img = Image.open(in_path).convert("RGB")
    
    # Create canvas
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    
    # Paste image (centered horizontally, top aligned at IMG_Y)
    # Image is 1224x936, scale to fit IMG_AREA_H if needed
    img_w, img_h = img.size
    if img_h > IMG_AREA_H:
        scale = IMG_AREA_H / img_h
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        img_w, img_h = new_w, new_h
    
    paste_x = (WIDTH - img_w) // 2
    paste_y = IMG_Y
    canvas.paste(img, (paste_x, paste_y))
    
    # Draw subtitles
    draw = ImageDraw.Draw(canvas)
    
    font_en = get_font(FONT_SIZE_EN, cn=False)
    font_en2 = get_font(FONT_SIZE_EN2, cn=False)
    font_cn = get_font(FONT_SIZE_CN, cn=True)
    font_cn2 = get_font(FONT_SIZE_CN2, cn=True)
    
    # English lines
    en_lines = wrap_text(scene.get("en", ""), font_en, WIDTH - 120)
    for i, line in enumerate(en_lines):
        bbox = font_en.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (WIDTH - w) // 2
        y = SUB_EN_Y[i]
        draw.text((x, y), line, font=font_en, fill=FONT_COLOR)
    
    # English 2 lines
    en2_lines = wrap_text(scene.get("en2", ""), font_en2, WIDTH - 120)
    for i, line in enumerate(en2_lines):
        bbox = font_en2.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (WIDTH - w) // 2
        y = SUB_EN2_Y[i]
        draw.text((x, y), line, font=font_en2, fill=FONT_COLOR)
    
    # Chinese lines
    cn_lines = wrap_text(scene.get("cn", ""), font_cn, WIDTH - 120)
    for i, line in enumerate(cn_lines):
        bbox = font_cn.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (WIDTH - w) // 2
        y = SUB_CN_Y[i]
        draw.text((x, y), line, font=font_cn, fill=FONT_COLOR)
    
    # Chinese 2 lines
    cn2_lines = wrap_text(scene.get("cn2", ""), font_cn2, WIDTH - 120)
    for i, line in enumerate(cn2_lines):
        bbox = font_cn2.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (WIDTH - w) // 2
        y = SUB_CN2_Y[i]
        draw.text((x, y), line, font=font_cn2, fill=FONT_COLOR)
    
    # Save
    out_path = os.path.join(OUTPUT_DIR, f"page{scene_idx:02d}.png")
    canvas.save(out_path, "PNG")
    print(f"  [OK] page{scene_idx:02d}.png saved")
    return True

def parse_script(path):
    """Parse script.md to extract scene texts."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    scenes = []
    blocks = re.split(r"## 场景(\d+)", content)
    for i in range(1, len(blocks), 2):
        num = int(blocks[i])
        body = blocks[i+1]
        entry = {"num": num}
        for prefix in ["en", "en2", "cn", "cn2"]:
            m = re.search(rf"\*\*{prefix}\*\*: (.+)", body)
            if m:
                entry[prefix] = m.group(1).strip()
            else:
                entry[prefix] = ""
        scenes.append(entry)
    scenes.sort(key=lambda x: x["num"])
    return scenes

def main():
    print("Creating Book-001 pages V4 (1920x1080 horizontal)...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    scenes = parse_script(SCRIPT_MD)
    print(f"Found {len(scenes)} scenes")
    
    for scene in scenes:
        create_page(scene["num"], scene)
    
    print(f"\nDone! {len(scenes)} pages created in {OUTPUT_DIR}/")
    print("Next: run gen_video_v4.py to generate videos")

if __name__ == "__main__":
    main()

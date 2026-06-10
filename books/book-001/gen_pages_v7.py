#!/usr/bin/env python3
"""
gen_pages_v7.py - Generate 13 picture book pages (1080x1920) EXACT match Book-021 format
Book-001: The Little Dancer's Dream / 小舞者的梦想
V2.5 Standard: CREAM background, 1024x768 illustration area, 4-line subtitles below image
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Constants (EXACT match Book-021 V2.5)
W, H = 1080, 1920
IMG_W, IMG_H = 1024, 768
WATERMARK_CROP = 45  # Crop bottom watermark area (px)
CREAM = (250, 246, 240)  # #FAF6F0
DARK_BROWN = (92, 64, 51)  # #5C4033

def get_font(size, is_cn=False):
    """Load font with fallback"""
    cn_fonts = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    en_fonts = [
        "C:/Windows/Fonts/comic.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    fonts_to_try = cn_fonts if is_cn else en_fonts
    for font_path in fonts_to_try:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                pass
    return ImageFont.load_default()

def wrap_text(text, max_width, font):
    """Wrap text to multiple lines if too wide (prevent overflow). Max 2 lines."""
    if not text:
        return []
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = font.getbbox(test_line)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines[:2]  # Max 2 lines only!

def create_page(scene_idx, scene, img_path):
    """Create one page (1080x1920) from one illustration. EXACT Book-021 format."""
    img = Image.open(img_path).convert("RGB")
    # Crop watermark (bottom 45px)
    if img.height > WATERMARK_CROP:
        img = img.crop((0, 0, img.width, img.height - WATERMARK_CROP))
    
    # Create canvas (cream white)
    canvas = Image.new("RGB", (W, H), CREAM)
    
    # Calculate img_y (dynamic vertical center in illustration area y=40~1400)
    img_area_h = 1400 - 40
    img_y = 40 + (img_area_h - IMG_H) // 2  # Dynamic centering formula
    
    # Paste illustration (pad to target size if needed, don't stretch)
    if img.size != (IMG_W, IMG_H):
        # Calculate padding to center the image
        pad_x = (IMG_W - img.width) // 2
        pad_y = (IMG_H - img.height) // 2
        padded_img = Image.new("RGB", (IMG_W, IMG_H), CREAM)
        padded_img.paste(img, (pad_x, pad_y))
        img = padded_img
    canvas.paste(img, ((W - IMG_W) // 2, img_y))
    
    # Draw subtitles
    draw = ImageDraw.Draw(canvas)
    
    # Fonts (EXACT match Book-021)
    font_en  = get_font(32, is_cn=False)
    font_en2 = get_font(28, is_cn=False)
    font_cn  = get_font(30, is_cn=True)
    font_cn2 = get_font(26, is_cn=True)
    
    # Subtitle area: y=1400~1920 (bottom 30%)
    # en (top of subtitle area)
    en_lines = wrap_text(scene["en"], W - 100, font_en)
    for i, line in enumerate(en_lines):
        bbox = font_en.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        y = 1450 + i * 50
        draw.text((x, y), line, fill=DARK_BROWN, font=font_en)
    
    # en2
    en2_lines = wrap_text(scene["en2"], W - 100, font_en2)
    for i, line in enumerate(en2_lines):
        bbox = font_en2.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        y = 1550 + i * 50
        draw.text((x, y), line, fill=DARK_BROWN, font=font_en2)
    
    # cn
    cn_lines = wrap_text(scene["cn"], W - 100, font_cn)
    for i, line in enumerate(cn_lines):
        bbox = font_cn.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        y = 1650 + i * 50
        draw.text((x, y), line, fill=DARK_BROWN, font=font_cn)
    
    # cn2
    cn2_lines = wrap_text(scene["cn2"], W - 100, font_cn2)
    for i, line in enumerate(cn2_lines):
        bbox = font_cn2.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        y = 1730 + i * 50
        draw.text((x, y), line, fill=DARK_BROWN, font=font_cn2)
    
    # Save
    out_path = f"pages_v7/page{scene_idx+1:02d}.png"
    canvas.save(out_path)
    print(f"  Created {out_path}")

# Scenes from book-001 script.md (13 scenes, each with en/en2/cn/cn2)
scenes = [
    {
        "en": "In the golden evening light, she watches the ballerinas dance with longing in her eyes.",
        "en2": "Her heart is already dancing, even before her feet learn the steps.",
        "cn": "金色夕阳下，她望着芭蕾舞者，眼中满是向往。",
        "cn2": "她的心早已在跳舞，即使双脚还未学会舞步。",
    },
    {
        "en": "She puts on her very first tutu, heart fluttering with excitement.",
        "en2": "Today, her own dance journey begins.",
        "cn": "她穿上人生第一条舞裙，心中充满期待。",
        "cn2": "今天，属于她自己的舞蹈旅程开始了。",
    },
    {
        "en": "The teacher gently guides her, but her body sways and wobbles.",
        "en2": "Standing still is harder than she ever imagined.",
        "cn": "老师温柔地指导她，可她的身体总是摇摇晃晃。",
        "cn2": "站稳比她想象的难多了。",
    },
    {
        "en": "She falls to the floor, tears streaming down her cheeks.",
        "en2": "Maybe dancing just isn't for her...",
        "cn": "她摔倒在地板上，泪水顺着脸颊流下来。",
        "cn2": "也许跳舞根本不适合她……",
    },
    {
        "en": "Her teacher kneels beside her, whispering words of encouragement.",
        "en2": "You haven't failed until you stop trying.",
        "cn": "老师跪在她身边，轻声说着鼓励的话。",
        "cn2": "只要不放弃，你就还没有失败。",
    },
    {
        "en": "At home, she practices in front of the mirror, again and again.",
        "en2": "No one is watching, but she refuses to give up.",
        "cn": "在家里，她在镜子前一遍又一遍地练习。",
        "cn2": "没有人在看，可她拒绝放弃。",
    },
    {
        "en": "Her toes are sore and blistered, she carefully puts on band-aids.",
        "en2": "Every blister is a step closer to her dream.",
        "cn": "脚尖疼痛起泡，她小心翼翼地贴上创可贴。",
        "cn2": "每一个水泡，都是离梦想更近一步。",
    },
    {
        "en": "She whispers to herself: I will not give up, no matter what.",
        "en2": "The hardest battles are the ones we fight inside.",
        "cn": "她悄悄对自己说：无论如何，我绝不放弃。",
        "cn2": "最艰难的战斗，是我们内心的战斗。",
    },
    {
        "en": "Practice is over, she runs and hugs her mother tightly.",
        "en2": "In her mother's arms, she feels safe enough to keep trying.",
        "cn": "练习结束了，她跑过去紧紧拥抱妈妈。",
        "cn2": "在妈妈怀里，她感到足够安全，可以继续努力。",
    },
    {
        "en": "After countless hours of practice, she finally dances with ease.",
        "en2": "Her body remembers what her heart never forgot.",
        "cn": "经过无数小时的练习，她终于能轻盈地跳舞了。",
        "cn2": "她的身体记住了她心里从未忘记的事。",
    },
    {
        "en": "Backstage before the show, her hands tremble with nervous excitement.",
        "en2": "This is the moment she has been waiting for.",
        "cn": "演出前的后台，她的双手因紧张兴奋而颤抖。",
        "cn2": "这是她一直等待的时刻。",
    },
    {
        "en": "Under the spotlight, she dances her heart out on the magnificent stage.",
        "en2": "Every eye is on her, and she is beautiful.",
        "cn": "聚光灯下，她在华丽的舞台上尽情舞蹈。",
        "cn2": "所有的目光都注视着她，而她是美丽的。",
    },
    {
        "en": "She stands victorious, crown on her head, dream come true.",
        "en2": "Every drop of persistence eventually crowns your dream.",
        "cn": "她胜利地站着，头戴皇冠，梦想成真。",
        "cn2": "点滴坚守，终为梦想加冕。",
    }
]

# User-provided images (13 pages in order)
user_images = [
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-39-999Z-fa6577dd.jpg',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-002Z-dd34705c.jpg',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-004Z-33238184.jpg',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-005Z-e2b54ea0.jpg',
    'D:/桌面/新建文件夹/page5.png',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-008Z-5a2cbb7d.jpg',
    'D:/桌面/新建文件夹/page 7.png',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-009Z-6f8bf705.jpg',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-011Z-af8b76e9.jpg',
    'D:/桌面/新建文件夹/page10.png',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-012Z-3ba63703.jpg',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-014Z-113adee4.jpg',
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-016Z-64cdfb32.jpg',
]

if __name__ == "__main__":
    print("Creating 13 picture book pages (Book-001 V7 - EXACT Book-021 format)...")
    os.makedirs("pages_v7", exist_ok=True)
    
    for i, scene in enumerate(scenes):
        create_page(i, scene, user_images[i])
    
    print("Done! 13 pages created in pages_v7/ directory.")

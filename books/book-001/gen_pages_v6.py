#!/usr/bin/env python3
"""
Generate book-001 pages v6 - EXACT match book-021 layout
Based on analysis:
- Canvas: 1080x1920
- Top margin: 393px (white)
- Image region: y=393 to y=1754 (height=1361)
- Bottom margin: y=1755 to y=1920 (height=165, white)
- Subtitle: overlaid on bottom of image region (around y=1731, small text)
"""

from PIL import Image, ImageDraw, ImageFont
import os

CANVAS_W, CANVAS_H = 1080, 1920
TOP_MARGIN = 393
IMAGE_Y_START = TOP_MARGIN  # 393
IMAGE_Y_END = 1754  # inclusive
IMAGE_H = IMAGE_Y_END - IMAGE_Y_START + 1  # 1362

# Subtitle: small text overlaid at bottom of image region
# From analysis: subtitle detected at y=1731-1754 (but that's just text pixels)
# Real subtitle box is likely y=1650 to y=1754 (100px height, overlaid on image)
SUBTITLE_Y_START = 1650
SUBTITLE_Y_END = 1754
SUBTITLE_H = SUBTITLE_Y_END - SUBTITLE_Y_START  # 104px

SUBTITLE_FONT_SIZE = 32
SUBTITLE_COLOR = (60, 60, 60)

def make_page(scene_path, subtitle_text, output_path):
    canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), (255, 255, 255))
    
    # Place scene image in image region (y=393-1754)
    if os.path.exists(scene_path):
        scene = Image.open(scene_path).convert('RGB')
        # Resize to fit IMAGE_H, preserving aspect, centered
        scene_w = int(scene.size[0] * IMAGE_H / scene.size[1])
        scene_h = IMAGE_H
        if scene_w > CANVAS_W:
            scene_w = CANVAS_W
            scene_h = int(scene.size[1] * scene_w / scene.size[0])
        scene_r = scene.resize((scene_w, scene_h), Image.LANCZOS)
        x_off = (CANVAS_W - scene_w) // 2
        y_off = IMAGE_Y_START  # top-aligned, not centered
        canvas.paste(scene_r, (x_off, y_off))
    
    # Draw subtitle overlaid on image bottom region
    if subtitle_text:
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', SUBTITLE_FONT_SIZE)
        except:
            font = ImageFont.load_default()
        
        # Draw text centered in subtitle region
        bbox = draw.textbbox((0, 0), subtitle_text, font=font)
        text_w = bbox[2] - bbox[0]
        x = (CANVAS_W - text_w) // 2
        y = SUBTITLE_Y_START + (SUBTITLE_H - SUBTITLE_FONT_SIZE) // 2
        draw.text((x, y), subtitle_text, font=font, fill=SUBTITLE_COLOR)
    
    canvas.save(output_path, 'PNG')
    print(f'Saved: {output_path}')

pages_data = [
    ('scene01.png', 'In a small village, there lived a little dancer named Lily.'),
    ('scene02.png', 'Lily practiced every day, even when it was difficult.'),
    ('scene03.png', 'Her dance teacher encouraged her to audition for the big show.'),
    ('scene04.png', 'Lily practiced day and night, perfecting every move.'),
    ('scene05.png', 'The day of the audition arrived. Lily was nervous but ready.'),
    ('scene06.png', 'She danced with all her heart, pouring her soul into the performance.'),
    ('scene07.png', 'The judges were amazed by her talent and passion.'),
    ('scene08.png', 'Lily got the lead role! She was overjoyed.'),
    ('scene09.png', 'The night of the big show, the theater was packed with people.'),
    ('scene10.png', 'Lily took a deep breath and stepped onto the stage.'),
    ('scene11.png', 'She danced like never before, captivating the entire audience.'),
    ('scene12.png', 'The crowd erupted in applause. Lily had achieved her dream.'),
    ('scene13.png', 'From that day on, Lily continued to dance, inspiring others.'),
]

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

output_dir = 'pages_v6'
os.makedirs(output_dir, exist_ok=True)

print('Generating book-001 pages v6 (exact match book-021 layout)...')
for i, (scene_file, subtitle) in enumerate(pages_data):
    output_path = f'{output_dir}/page{str(i+1).zfill(2)}.png'
    make_page(user_images[i], subtitle, output_path)

print('Done! Generated 13 pages in pages_v6/')

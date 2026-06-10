#!/usr/bin/env python3
"""
Generate book-001 pages v5 - Vertical 1080x1920 format (matching book-021 template)
- Canvas: 1080x1920 (vertical)
- Image region: top portion (y=0 to y=~1200)
- Subtitle region: bottom portion (y=1470 to y=1754, matching book-021)
- User's 13 images are horizontal, will be placed in top region preserving aspect ratio
"""

from PIL import Image, ImageDraw, ImageFont
import os, textwrap

# Book-021 template analysis:
# - Canvas: 1080x1920
# - Image region: y=393 to y=1045 (height=652)
# - Subtitle region: y=1470 to y=1754 (height=284)
# So: top margin ~393, image height ~652, middle gap ~425, subtitle start ~1470

CANVAS_W, CANVAS_H = 1080, 1920
IMAGE_REGION_TOP = 0  # image starts at top
IMAGE_REGION_H = 1200  # image occupies top 1200px
SUBTITLE_REGION_TOP = 1470  # subtitle starts at y=1470 (matching book-021)
SUBTITLE_REGION_H = 284  # subtitle region height (matching book-021)

# Subtitle style (matching book-021)
SUBTITLE_FONT_SIZE = 36
SUBTITLE_COLOR = (50, 50, 50)  # dark gray
SUBTITLE_LINE_SPACING = 8

def make_page(scene_path, subtitle_text, output_path):
    """Create one page: vertical 1080x1920, image on top, subtitle on bottom."""
    # Create canvas (white)
    canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Load and place scene image (horizontal) in top region
    if os.path.exists(scene_path):
        scene = Image.open(scene_path).convert('RGB')
        # Resize to fit IMAGE_REGION_H, preserving aspect ratio, centered
        scene_h = IMAGE_REGION_H
        scene_w = int(scene.size[0] * scene_h / scene.size[1])
        if scene_w > CANVAS_W:
            scene_w = CANVAS_W
            scene_h = int(scene.size[1] * scene_w / scene.size[0])
        scene_resized = scene.resize((scene_w, scene_h), Image.LANCZOS)
        x_offset = (CANVAS_W - scene_w) // 2
        y_offset = IMAGE_REGION_TOP
        canvas.paste(scene_resized, (x_offset, y_offset))
    
    # Draw subtitle in bottom region (matching book-021 position)
    if subtitle_text:
        try:
            font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', SUBTITLE_FONT_SIZE)
        except:
            font = ImageFont.load_default()
        
        # Word wrap subtitle text to fit canvas width
        max_width = CANVAS_W - 80  # 40px margin each side
        words = subtitle_text.split()
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Draw lines centered in subtitle region
        line_height = SUBTITLE_FONT_SIZE + SUBTITLE_LINE_SPACING
        total_height = len(lines) * line_height
        start_y = SUBTITLE_REGION_TOP + (SUBTITLE_REGION_H - total_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0]
            x = (CANVAS_W - line_w) // 2
            y = start_y + i * line_height
            draw.text((x, y), line, font=font, fill=SUBTITLE_COLOR)
    
    canvas.save(output_path, 'PNG')
    print(f'Saved: {output_path}')

# Script data (from script.md)
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

# Input: user's 13 images (horizontal) - need to find them
# They were copied to clipboard-images with specific names
user_images = [
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-39-999Z-fa6577dd.jpg',  # page1
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-002Z-dd34705c.jpg',  # page2
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-004Z-33238184.jpg',  # page3
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-005Z-e2b54ea0.jpg',  # page4
    'D:/桌面/新建文件夹/page5.png',  # page5
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-008Z-5a2cbb7d.jpg',  # page6
    'D:/桌面/新建文件夹/page 7.png',  # page7
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-009Z-6f8bf705.jpg',  # page8
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-011Z-af8b76e9.jpg',  # page9
    'D:/桌面/新建文件夹/page10.png',  # page10
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-012Z-3ba63703.jpg',  # page11
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-014Z-113adee4.jpg',  # page12
    'C:/Users/Mary/.workbuddy/clipboard-images/clipboard-2026-06-09T14-23-40-016Z-64cdfb32.jpg',  # page13
]

output_dir = 'pages_v5'
os.makedirs(output_dir, exist_ok=True)

print('Generating book-001 pages v5 (vertical 1080x1920, matching book-021 template)...')
for i, (scene_file, subtitle) in enumerate(pages_data):
    img_path = user_images[i]
    output_path = f'{output_dir}/page{str(i+1).zfill(2)}.png'
    make_page(img_path, subtitle, output_path)

print('Done! Generated 13 pages in pages_v5/')

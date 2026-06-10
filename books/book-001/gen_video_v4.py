#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Book-001 video V4.
Input: pages_v4/*.png + E:/.../audio_lines_v2/*.mp3
Output: video_us_v4.mp4, video_uk_v4.mp4
"""

import os
import json
import subprocess

PAGES_DIR = "pages_v7"
AUDIO_DIR = "E:/WorkBuddy/picture-books/book-001/audio_lines_v2"
OUTPUT_DIR = "."
SEGMENTS_DIR = "segments_v5"
FFMPEG = "ffmpeg"

def get_duration(audio_path):
    """Get audio duration using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])

def create_segment(page_path, audio_path, out_path):
    """Create video segment: static image + audio."""
    dur = get_duration(audio_path)
    cmd = [
        FFMPEG, "-y",
        "-loop", "1",
        "-i", page_path,
        "-i", audio_path,
        "-c:v", "libx264", "-crf", "18", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuvj420p",
        "-t", str(dur),
        "-avoid_negative_ts", "1",
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERR] Failed: {out_path}")
        print(result.stderr[-500:])
        return False
    return True

def concat_segments(segment_paths, out_path):
    """Concat video segments into final video."""
    list_file = os.path.join(SEGMENTS_DIR, "concat_list.txt")
    with open(list_file, "w") as f:
        for p in segment_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
    
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERR] Concat failed: {out_path}")
        print(result.stderr[-500:])
        return False
    return True

def main():
    os.makedirs(SEGMENTS_DIR, exist_ok=True)
    
    for lang in ["us", "uk"]:
        print(f"\n[INFO] Processing {lang.upper()} version...")
        segments = []
        
        for i in range(1, 14):
            num = i
            page_path = os.path.join(PAGES_DIR, f"page{num:02d}.png")
            audio_path = os.path.join(AUDIO_DIR, f"{num:02d}_{lang}.mp3")
            segment_path = os.path.join(SEGMENTS_DIR, f"seg_{num:02d}_{lang}.mp4")
            
            if not os.path.exists(page_path):
                print(f"[WARN] Missing page: {page_path}")
                continue
            if not os.path.exists(audio_path):
                print(f"[WARN] Missing audio: {audio_path}")
                continue
            
            dur = get_duration(audio_path)
            print(f"[INFO] Creating segment {num:02d} {lang} (duration={dur:.2f}s)...", end=" ")
            if create_segment(page_path, audio_path, segment_path):
                print("OK")
                segments.append(segment_path)
            else:
                print("FAILED")
        
        # Concat segments
        out_path = os.path.join(OUTPUT_DIR, f"video_{lang}.mp4")
        print(f"\n[INFO] Concatenating {len(segments)} segments -> {out_path}...")
        if concat_segments(segments, out_path):
            total = sum(get_duration(s) for s in segments)
            print(f"[OK] Final video: {out_path} (total duration: {total:.2f}s)")
        else:
            print(f"[ERR] Failed to create {out_path}")
    
    print("\n[OK] All videos generated!")

if __name__ == "__main__":
    main()

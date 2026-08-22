"""
Velocity Japanese - Video Builder & Assembler (V3 - Scenario Art & Website Sync)
Combines rendered scene cards and audio tracks into professional MP4 videos using FFmpeg.
"""
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from config import (
    OUTPUT_DIR,
    VERTICAL_WIDTH,
    VERTICAL_HEIGHT,
    HORIZONTAL_WIDTH,
    HORIZONTAL_HEIGHT,
    DEFAULT_FPS,
    CHANNEL_NAME,
    WEBSITE_URL,
    CTA_TEXT,
    FOOTER_TAG,
    BGM_DIR
)
from renderer import (
    render_item_frame,
    render_outro_frame,
    render_thumbnail,
    fetch_scenario_background
)

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def assemble_scene_video(frame_img_path: Path, audio_path: Path, output_path: Path, fps: int = DEFAULT_FPS) -> Path:
    """Combine a single image frame and its audio into an MP4 video clip."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-framerate", str(fps),
        "-i", str(frame_img_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        str(output_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_path

def build_full_video(
    lesson: dict,
    scenes_audio: List[Dict],
    session_dir: Path,
    is_vertical: bool = True,
    bgm_path: Optional[Path] = None
) -> Dict:
    """
    Build the complete Japanese lesson video.
    Returns metadata and output file paths.
    """
    frames_dir = session_dir / "frames"
    clips_dir = session_dir / "clips"
    frames_dir.mkdir(parents=True, exist_ok=True)
    clips_dir.mkdir(parents=True, exist_ok=True)
    
    width = VERTICAL_WIDTH if is_vertical else HORIZONTAL_WIDTH
    height = VERTICAL_HEIGHT if is_vertical else HORIZONTAL_HEIGHT
    
    # 1. Fetch / Cache Thematic Scenario Background Art
    art_prompt = lesson.get("art_prompt") or f"beautiful {lesson.get('title', 'japan')} anime aesthetic clean art"
    bg_cache_file = session_dir / "scenario_bg.jpg"
    bg_img = fetch_scenario_background(art_prompt, bg_cache_file, width=width, height=height)
    
    total_duration = sum(s["duration"] for s in scenes_audio)
    elapsed_time = 0.0
    
    scene_clip_paths = []
    
    # 2. Render frames and assemble each scene
    for i, scene in enumerate(scenes_audio):
        scene_type = scene["type"]
        dur = scene["duration"]
        progress = elapsed_time / max(1.0, total_duration)
        
        frame_path = frames_dir / f"frame_{i:03d}_{scene_type}.jpg"
        clip_path = clips_dir / f"clip_{i:03d}_{scene_type}.mp4"
        
        if scene_type == "item":
            img = render_item_frame(
                item=scene["item_data"],
                index=scene["index"],
                total=scene["total_items"],
                width=width,
                height=height,
                progress=progress,
                bg_img=bg_img
            )
        elif scene_type == "outro":
            img = render_outro_frame(
                title=lesson.get("title", "Japanese Lesson"),
                width=width,
                height=height,
                progress=1.0,
                bg_img=bg_img
            )
        else:
            img = render_item_frame(
                item=lesson.get("items", [{}])[0],
                index=1,
                total=len(lesson.get("items", [{}])),
                width=width,
                height=height,
                progress=0.0,
                bg_img=bg_img
            )
            
        img.save(frame_path, quality=96)
        assemble_scene_video(frame_path, scene["audio_path"], clip_path)
        scene_clip_paths.append(clip_path)
        
        elapsed_time += dur

    # 3. Concat all scene MP4 clips together
    concat_manifest = session_dir / "concat_clips.txt"
    with open(concat_manifest, "w", encoding="utf-8") as f:
        for clip in scene_clip_paths:
            safe_p = str(clip.resolve()).replace("\\", "/")
            f.write(f"file '{safe_p}'\n")
            
    raw_video_path = session_dir / "raw_video.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_manifest),
        "-c", "copy",
        str(raw_video_path)
    ], capture_output=True, check=True)
    
    # 4. Final Video Output Path
    final_video_name = "VelocityJapanese_Short.mp4" if is_vertical else "VelocityJapanese_Video.mp4"
    final_video_path = session_dir / final_video_name
    
    if not bgm_path:
        bgm_candidates = list(BGM_DIR.glob("*.mp3")) + list(BGM_DIR.glob("*.wav"))
        if bgm_candidates:
            bgm_path = bgm_candidates[0]
            
    if bgm_path and bgm_path.exists():
        cmd_bgm = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-stream_loop", "-1",
            "-i", str(bgm_path),
            "-filter_complex",
            "[0:a]volume=1.0[a0];[1:a]volume=0.08[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(final_video_path)
        ]
        subprocess.run(cmd_bgm, capture_output=True, check=True)
    else:
        import shutil
        shutil.copy2(raw_video_path, final_video_path)
        
    # 5. Generate Thumbnail (First item card with 0 progress)
    thumbnail_path = session_dir / "thumbnail.jpg"
    thumb_img = render_thumbnail(lesson, width, height, bg_img=bg_img)
    thumb_img.save(thumbnail_path, quality=96)
    
    # 6. Rich Metadata with Website Link & Hashtags
    title = lesson.get("title", "Learn Japanese Daily")
    items = lesson.get("items", [])
    
    tags = [
        "Velocity Japanese", "velocityjapanese.com", "Learn Japanese", "Japanese Vocabulary",
        "JLPT N5", "Japanese Kanji", "Japanese Pronunciation",
        "Japanese For Beginners", "Hiragana", "Romaji", "Japanese Phrases"
    ]
    
    hashtags = "#VelocityJapanese #LearnJapanese #JapaneseLesson #JLPT #JLPTN5 #JapaneseVocabulary #JapanesePhrases #Nihongo #Reels #Shorts"
    
    desc_lines = [
        f"🇯🇵 {title} | Velocity Japanese",
        "",
        "Master essential Japanese vocabulary, Kanji readings, and natural pronunciation!",
        "",
        "📚 In This Video:",
    ]
    for idx, it in enumerate(items, 1):
        k = it.get('kanji', '')
        h = it.get('hiragana', '')
        r = it.get('romaji', '')
        e = it.get('english', '')
        desc_lines.append(f"  {idx}. {k} ({h} - {r}) : {e}")
        
    desc_lines.extend([
        "",
        f"🌐 Free PDF Guides & Lessons: https://{WEBSITE_URL}",
        "🔔 Follow Velocity Japanese for daily Japanese lessons, Kanji breakdowns, and study tips!",
        "📘 Facebook Page: Velocity Japanese",
        "",
        hashtags
    ])
    
    metadata = {
        "title": f"🇯🇵 {title} - Japanese Lesson | Velocity Japanese",
        "description": "\n".join(desc_lines),
        "website": WEBSITE_URL,
        "tags": tags,
        "video_path": str(final_video_path.resolve()),
        "thumbnail_path": str(thumbnail_path.resolve()),
        "duration_seconds": total_duration,
        "item_count": len(items),
        "aspect_ratio": "9:16" if is_vertical else "16:9"
    }
    
    metadata_path = session_dir / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        
    desc_path = session_dir / "description.txt"
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write(metadata["description"])
        
    return metadata

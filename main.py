"""
Velocity Japanese - Video Generator & Social Publisher Bot (V3)
Main execution script for creating and publishing automated Japanese learning videos for Facebook Reels & YouTube Shorts.
"""
import os
import sys
import argparse
import asyncio
import time
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import (
    OUTPUT_DIR,
    CHANNEL_NAME,
    WEBSITE_URL,
    CURATED_TOPICS,
    DEFAULT_JA_VOICE,
    DEFAULT_EN_VOICE,
    DEFAULT_ITEM_COUNT
)
from content_generator import fetch_lesson_from_ai, get_preset_image_lesson, get_next_fresh_category_and_topic
from audio_engine import generate_lesson_audio
from video_builder import build_full_video
from publisher import publish_to_facebook

def create_video_session(
    topic: str = None,
    image_path: str = None,
    preset_idx: int = None,
    item_count: int = DEFAULT_ITEM_COUNT,
    is_vertical: bool = True,
    ja_voice: str = DEFAULT_JA_VOICE,
    en_voice: str = DEFAULT_EN_VOICE,
    include_intro: bool = False,
    auto_publish: bool = False
) -> dict:
    """Run end-to-end pipeline to generate a Japanese lesson video."""
    print("=" * 65)
    print(f"🎬 VELOCITY JAPANESE - REELS / SHORTS GENERATOR")
    print(f"   Brand: {CHANNEL_NAME} ({WEBSITE_URL})")
    print(f"   Format: {'Vertical (9:16)' if is_vertical else 'Horizontal (16:9)'}")
    print("=" * 65)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Fetch Lesson Content
    print("\n[Step 1/3] Generating Fresh Lesson Concept & Artwork...")
    if image_path:
        print(f" -> Extracting lesson from inspiration image: {image_path}")
        lesson = get_preset_image_lesson(Path(image_path).name, item_count=item_count)
    elif preset_idx is not None and 0 <= preset_idx < len(CURATED_TOPICS):
        print(f" -> Using curated preset lesson #{preset_idx + 1}")
        lesson = dict(CURATED_TOPICS[preset_idx])
        lesson["items"] = lesson["items"][:item_count]
    else:
        lesson = fetch_lesson_from_ai(topic=topic, item_count=item_count)
        
    slug_title = "".join(c for c in lesson.get("title", "lesson") if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    session_dir = OUTPUT_DIR / f"{timestamp}_{slug_title[:30]}"
    session_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"   Title:    {lesson.get('title')}")
    print(f"   Category: {lesson.get('category', 'Japanese')}")
    print(f"   Art Idea: {lesson.get('art_prompt', 'Tokyo Aesthetic')}")
    print(f"   Cards ({len(lesson.get('items', []))} items):")
    for i, it in enumerate(lesson.get("items", []), 1):
        print(f"     {i}. {it.get('kanji')} 【{it.get('hiragana')}】 - {it.get('english')}")

    # 2. Synthesize High-Definition Audio with 100% Phonetic Accuracy
    print("\n[Step 2/3] Synthesizing Japanese & English Voice Audio (edge-tts)...")
    print(f"   Japanese Voice: {ja_voice} (Phonetic Hiragana for 100% precision)")
    print(f"   English Voice:  {en_voice}")
    scenes_audio = asyncio.run(generate_lesson_audio(
        lesson=lesson,
        session_dir=session_dir,
        ja_voice=ja_voice,
        en_voice=en_voice,
        include_intro=include_intro
    ))
    total_sec = sum(s["duration"] for s in scenes_audio)
    print(f"   Audio complete: {len(scenes_audio)} scenes (~{total_sec:.1f}s duration)")

    # 3. Render High-Resolution Graphics & Assemble Video
    print("\n[Step 3/3] Rendering 1080p Cards with Scenario Backdrop & Assembling Video...")
    result = build_full_video(
        lesson=lesson,
        scenes_audio=scenes_audio,
        session_dir=session_dir,
        is_vertical=is_vertical
    )

    # 4. Optional Auto-Publish to Facebook with Pinned Comment
    if auto_publish:
        print("\n[Publishing] Publishing video to Velocity Japanese on Facebook...")
        pub_res = publish_to_facebook(Path(result["video_path"]), lesson)
        if pub_res:
            result["facebook_publish"] = pub_res

    # 5. Summary & Links
    print("\n🎉 Video Pipeline Complete!")
    print("-" * 65)
    print(f"📹 Final Video:   {result['video_path']}")
    print(f"🖼️ Thumbnail:     {result['thumbnail_path']}")
    print(f"📄 Metadata:      {session_dir / 'metadata.json'}")
    print(f"⏱️ Duration:      {result['duration_seconds']:.1f} seconds (Target: ~35-45s)")
    print(f"🌐 Official Site: https://{WEBSITE_URL}")
    print("-" * 65)
    return result

def main():
    parser = argparse.ArgumentParser(description="Velocity Japanese Video Generator Bot")
    parser.add_argument("--topic", type=str, default=None, help="Custom Japanese topic (e.g. 'Ordering Ramen', 'Akihabara Shopping')")
    parser.add_argument("--image", type=str, default=None, help="Path to inspiration image to extract/parse lesson")
    parser.add_argument("--preset", type=int, default=None, help="Use preset lesson (0: Days of Week, 1: N5 Kanji, 2: Daily Phrases)")
    parser.add_argument("--count", type=int, default=DEFAULT_ITEM_COUNT, help="Number of items to generate (default: 3)")
    parser.add_argument("--horizontal", action="store_true", help="Generate 16:9 horizontal video instead of 9:16 vertical short")
    parser.add_argument("--batch", type=int, default=1, help="Number of distinct videos to generate in batch")
    parser.add_argument("--auto", action="store_true", help="Automatically pick a fresh daily topic across categories")
    parser.add_argument("--with-intro", action="store_true", help="Include title intro slide (default: False)")
    parser.add_argument("--publish", action="store_true", help="Automatically publish video to Facebook with pinned comment")
    
    args = parser.parse_args()
    is_vertical = not args.horizontal
    
    if args.batch > 1:
        print(f"🚀 Starting batch generation of {args.batch} videos...")
        for b_idx in range(1, args.batch + 1):
            print(f"\n==================== BATCH [{b_idx}/{args.batch}] ====================")
            create_video_session(
                topic=args.topic,
                item_count=args.count,
                is_vertical=is_vertical,
                include_intro=args.with_intro,
                auto_publish=args.publish
            )
            time.sleep(2)
        print(f"\n✨ Batch complete! Generated {args.batch} videos in {OUTPUT_DIR}")
        return

    # Single run
    create_video_session(
        topic=args.topic,
        image_path=args.image,
        preset_idx=args.preset,
        item_count=args.count,
        is_vertical=is_vertical,
        include_intro=args.with_intro,
        auto_publish=args.publish
    )

if __name__ == "__main__":
    main()

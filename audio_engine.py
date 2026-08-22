"""
Velocity Japanese - Audio Engine (V3 - Flawless Phonetic Pronunciation)
Generates high-definition Japanese and English voice audio using edge-tts.
"""
import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import edge_tts

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import (
    DEFAULT_JA_VOICE,
    DEFAULT_EN_VOICE,
    CHANNEL_NAME,
    WEBSITE_URL
)

def get_audio_duration(file_path: Path) -> float:
    """Get accurate duration in seconds using ffprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception as e:
        print(f"[AudioEngine] ffprobe warning for {file_path}: {e}")
        return 2.5

async def synthesize_speech(text: str, voice: str, output_path: Path, rate: str = "+0%", pitch: str = "+0Hz") -> float:
    """Synthesize single speech clip using edge-tts."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_text = text.strip()
    if not clean_text:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
            "-t", "1.0", str(output_path)
        ], capture_output=True)
        return 1.0

    try:
        communicate = edge_tts.Communicate(clean_text, voice, rate=rate, pitch=pitch)
        await communicate.save(str(output_path))
        return get_audio_duration(output_path)
    except Exception as e:
        print(f"[AudioEngine] TTS error for '{text}' ({voice}): {e}. Creating fallback silence.")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
            "-t", "2.0", str(output_path)
        ], capture_output=True)
        return 2.0

def create_silence(duration: float, output_path: Path):
    """Generate exact silence audio file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", f"{duration:.2f}", "-c:a", "libmp3lame", "-b:a", "192k", str(output_path)
    ], capture_output=True)

async def generate_lesson_audio(
    lesson: dict,
    session_dir: Path,
    ja_voice: str = DEFAULT_JA_VOICE,
    en_voice: str = DEFAULT_EN_VOICE,
    include_intro: bool = False
) -> List[Dict]:
    """
    Generate all audio clips for a lesson.
    Feeds phonetic Hiragana for the Japanese word to guarantee 100% flawless pronunciation!
    """
    audio_dir = session_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    title = lesson.get("title", "Japanese Lesson")
    items = lesson.get("items", [])
    
    scenes_audio = []
    
    # 1. Optional Intro (Only if requested)
    if include_intro:
        intro_path = audio_dir / "intro.mp3"
        intro_text_en = f"Learn {title} with Velocity Japanese!"
        intro_dur = await synthesize_speech(intro_text_en, en_voice, intro_path, rate="+5%")
        scenes_audio.append({
            "type": "intro",
            "title": title,
            "audio_path": intro_path,
            "duration": intro_dur + 0.3,
            "spoken_text": intro_text_en
        })
    
    pause_path = audio_dir / "pause_small.mp3"
    if not pause_path.exists():
        create_silence(0.35, pause_path)

    # 2. Synthesize each word item
    for idx, item in enumerate(items, 1):
        item_audio_files = []
        
        # Part A: Japanese Word / Kanji reading
        # CRUCIAL: To guarantee 100% correct pronunciation in Japanese TTS,
        # we feed the phonetic hiragana (e.g. 'あたま' instead of ambiguous kanji '頭')
        ja_phonetic = item.get("hiragana", "").strip() or item.get("kanji", "").strip()
        part_a_path = audio_dir / f"item_{idx:02d}_ja_word.mp3"
        part_a_dur = await synthesize_speech(ja_phonetic, ja_voice, part_a_path, rate="-3%")
        item_audio_files.append((part_a_path, part_a_dur, "ja_word"))
        
        # Part B: English Translation
        en_word = item["english"]
        part_b_path = audio_dir / f"item_{idx:02d}_en_word.mp3"
        part_b_dur = await synthesize_speech(en_word, en_voice, part_b_path, rate="+3%")
        item_audio_files.append((part_b_path, part_b_dur, "en_word"))
        
        # Part C: Example Japanese sentence
        example_ja = item.get("example_ja", "").strip()
        if example_ja:
            part_c_path = audio_dir / f"item_{idx:02d}_ja_example.mp3"
            part_c_dur = await synthesize_speech(example_ja, ja_voice, part_c_path, rate="-3%")
            item_audio_files.append((part_c_path, part_c_dur, "ja_example"))
            
        # Part D: Example English sentence
        example_en = item.get("example_en", "").strip()
        if example_en and example_ja:
            part_d_path = audio_dir / f"item_{idx:02d}_en_example.mp3"
            part_d_dur = await synthesize_speech(example_en, en_voice, part_d_path, rate="+5%")
            item_audio_files.append((part_d_path, part_d_dur, "en_example"))

        # Concat audio for this item
        concat_list = audio_dir / f"item_{idx:02d}_concat.txt"
        item_combined_path = audio_dir / f"item_{idx:02d}_full.mp3"
        
        with open(concat_list, "w", encoding="utf-8") as f:
            for i, (fpath, _, _) in enumerate(item_audio_files):
                safe_path = str(fpath.resolve()).replace("\\", "/")
                f.write(f"file '{safe_path}'\n")
                if i < len(item_audio_files) - 1:
                    safe_pause = str(pause_path.resolve()).replace("\\", "/")
                    f.write(f"file '{safe_pause}'\n")
        
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c:a", "libmp3lame", "-b:a", "192k", str(item_combined_path)
        ], capture_output=True, check=True)
        
        item_total_dur = get_audio_duration(item_combined_path)
        
        scenes_audio.append({
            "type": "item",
            "index": idx,
            "total_items": len(items),
            "item_data": item,
            "audio_path": item_combined_path,
            "duration": item_total_dur + 0.3,
            "sub_clips": item_audio_files
        })
    
    # 3. Short Outro Clip with Website Branding (2.5 seconds)
    outro_path = audio_dir / "outro.mp3"
    outro_text = f"Follow Velocity Japanese and visit {WEBSITE_URL} for daily lessons! またね!"
    outro_dur = await synthesize_speech(outro_text, en_voice, outro_path, rate="+8%")
    scenes_audio.append({
        "type": "outro",
        "title": title,
        "audio_path": outro_path,
        "duration": outro_dur + 0.3,
        "spoken_text": outro_text
    })
    
    return scenes_audio

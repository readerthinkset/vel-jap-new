# 🌸 Velocity Japanese - Automated Short/Reel Video Generator Bot

An automated AI video production bot for **Velocity Japanese** (Facebook & YouTube). Generates 1080p Japanese learning videos with native Japanese pronunciation, English voice explanations, Furigana & Romaji readings, massive high-contrast example sentences, and channel branding.

---

## ⚡ What’s New in V2

- ⚡ **Instant Hook (No Intro)**: Videos start immediately on Word 1 at second 0 for maximum retention on YouTube Shorts & Facebook Reels.
- 🔍 **Massive High-Contrast Typography**: Kanji at **160px**, Hiragana at **44px**, English badges at **48px**, and Example sentences at **56px** with high-contrast emerald translation for effortless mobile reading.
- ⏱️ **Optimized Duration (~35 to 45 Seconds)**: Every video is 3 punchy, high-value vocabulary/Kanji cards plus a 2.5s outro, hitting the ~35-45s sweet spot.
- 🔁 **Forever-Run Daily Auto-Pilot**: Tracks generated concepts in `history.json` and automatically creates a new topic every single day from a 50+ topic bank or via Pollinations AI.
- 🎌 **Bilingual Audio Engine (`edge-tts`)**:
  - Japanese Native Speaker (`ja-JP-NanamiNeural` / `ja-JP-KeitaNeural`) for Kanji, words, and example sentences.
  - English Narrator (`en-US-AndrewNeural` / `en-US-AvaNeural`) for translations.

---

## 📁 Directory Structure

```
Japanese/
├── .github/workflows/
│   └── daily_generate.yml      # Scheduled GitHub Actions automated workflow
├── assets/
│   └── bgm/                    # Optional background music tracks (.mp3)
├── fonts/
│   ├── NotoSansJP-Bold.ttf     # Japanese Kanji & Kana font
│   ├── NotoSansJP-Regular.ttf
│   ├── DejaVuSans-Bold.ttf
│   └── DejaVuSans.ttf
├── output/                     # Generated videos, thumbnails, and metadata
├── history.json                # Daily topic tracking (prevents duplicates)
├── audio_engine.py             # edge-tts voice synthesis pipeline (No intro, snappy)
├── config.py                   # Branding, 50+ topic bank, voices, colors
├── content_generator.py        # Pollinations AI lesson generator & history manager
├── main.py                     # Main CLI controller and batch generator
├── renderer.py                 # Pillow 1080p graphic card rendering
├── video_builder.py            # FFmpeg assembly and BGM mixing
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows 1-click launcher
└── README.md
```

---

## ⚡ How to Run

### 1. Interactive 1-Click Menu (Windows)
Double-click [`run.bat`](file:///C:/Users/kreg9/Downloads/kreggscode/agy%20cli/bots/Youtube%20bots/Japanese/run.bat) to launch the generator.

### 2. Daily Auto-Pilot (Generates a Brand New Concept Every Run)
```bash
python main.py --auto
```

### 3. Generate from Presets (~35s duration)
```bash
python main.py --preset 0   # Days of the Week
python main.py --preset 1   # Must-Know JLPT N5 Kanji
python main.py --preset 2   # Everyday Essential Phrases
```

### 4. Generate from Custom Topics (Powered by AI)
```bash
python main.py --topic "Ordering at Tokyo Ramen Shops"
python main.py --topic "Japanese Izakaya Dining Phrases"
```

### 5. Generate from Inspiration Images
```bash
python main.py --image "C:\Users\kreg9\Downloads\photo_6075568155066569876_y.jpg"
```

### 6. Batch Generation
```bash
python main.py --batch 3 --auto
```

---

## ☁️ GitHub Actions Daily Publishing

Push this folder to GitHub. The workflow in [`.github/workflows/daily_generate.yml`](file:///C:/Users/kreg9/Downloads/kreggscode/agy%20cli/bots/Youtube%20bots/Japanese/.github/workflows/daily_generate.yml) runs automatically on schedule to generate fresh daily videos and upload them to GitHub Artifacts.

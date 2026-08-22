# 🌸 Velocity Japanese - Automated Daily Video Generator & Social Media Publisher

Automated video production and publishing engine for **Velocity Japanese** ([velocityjapanese.com](https://velocityjapanese.com)).

Generates 1080p high-retention Japanese learning shorts/reels with native Japanese TTS pronunciation, Furigana & Romaji readings, massive example sentences, AI-generated anime backdrop artwork, and automatically publishes to the **Velocity Japanese Facebook Page** & **Instagram** with structured **Pinned First Comments**.

---

## ⚡ Highlights

- ⚡ **Instant Hook (0s Start)**: Starts directly on Word 1 without slow intro cards for maximum retention on Reels & Shorts.
- 🎌 **100% Phonetic Accuracy**: Synthesizes pure Hiragana readings in `ja-JP-NanamiNeural` so every Kanji is pronounced with native Japanese precision.
- 🎨 **AI Scenario Artwork**: Renders themed anime/Japanese backdrops for each daily concept.
- 🔍 **Massive Typography**: 160px Kanji, 44px Furigana, 48px English badges, and 52px example sentences with character-level wrapping (zero text cropping).
- 🌐 **Branding & Website Call-to-Action**: Displays `velocityjapanese.com` in header, footer, outro, description, and pinned comments.
- 💬 **Automated Pinned Comments**: Posts the full lesson recap and website link as the first comment on Facebook.
- 🔁 **Forever-Run Auto-Pilot**: Rotates across 10 distinct categories and tracks daily concepts in `history.json` to prevent duplicates.
- ☁️ **GitHub Actions Integration**: Runs on a daily schedule (`0 6 * * *`), commits updated `history.json` back to GitHub, and stores video artifacts.

---

## 📁 Repository Structure

```
vel-jap-new/
├── .github/workflows/
│   └── daily_generate.yml      # Scheduled GitHub Actions auto-publish workflow
├── assets/
│   └── bgm/                    # Optional background music tracks (.mp3)
├── fonts/
│   ├── NotoSansJP-Bold.ttf     # Japanese Kanji & Kana fonts
│   ├── NotoSansJP-Regular.ttf
│   ├── DejaVuSans-Bold.ttf
│   └── DejaVuSans.ttf
├── history.json                # Daily topic tracking (auto-committed on each run)
├── audio_engine.py             # edge-tts voice synthesis (Phonetic Hiragana)
├── config.py                   # Categorized topic bank, voices, colors, URLs
├── content_generator.py        # Pollinations AI lesson generator & history manager
├── main.py                     # Main CLI controller and batch generator
├── publisher.py                # Facebook Page & Instagram video uploader + pinned comments
├── renderer.py                 # Pillow 1080p card renderer with scenario art
├── video_builder.py            # FFmpeg assembly and audio-video mixing
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows 1-click launcher
└── README.md
```

---

## ⚡ How to Run Locally

### 1. 1-Click Interactive Menu (Windows)
Double-click `run.bat` to launch the menu:
- Daily Auto-Pilot
- Presets (Days of the Week, JLPT N5 Kanji, Daily Phrases)
- Custom Topic AI generation
- 3-Video Batch generation

### 2. Daily Auto-Pilot
```bash
python main.py --auto
```

### 3. Generate & Publish to Facebook with Pinned Comment
```bash
python main.py --auto --publish
```

### 4. Custom Topic Mode
```bash
python main.py --topic "Ordering at Tokyo Ramen Shops"
```

---

## 🔑 GitHub Actions Secrets Setup

To enable automated daily publishing on GitHub Actions, add these repository secrets:
- `POLLINATIONS_API_KEY`: Your Pollinations AI Key (`sk_K98...`)
- `META_ACCESS_TOKEN`: Long-lived Meta User Access Token
- `FB_PAGE_ID`: `1048385991689324` (Velocity Japanese)

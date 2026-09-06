"""
Velocity Japanese - Content & Lesson Generator (V3 - Category Diversity & Scenario Art)
Generates unique Japanese lessons daily across 10 categories using Pollinations AI with history tracking.
"""
import json
import random
import re
from datetime import datetime
from pathlib import Path
import requests

from config import (
    POLLINATIONS_API_KEY,
    POLLINATIONS_ENDPOINT,
    AI_MODEL,
    CURATED_TOPICS,
    CATEGORIZED_TOPICS,
    HISTORY_FILE,
    DEFAULT_ITEM_COUNT
)

def clean_text(text: str, is_romaji: bool = False, is_japanese: bool = False) -> str:
    """Clean and sanitize text string, preventing emoji artifacts or broken glyphs."""
    if not text:
        return ""
    text = re.sub(r'[\r\n]+', ' ', text)
    # Remove supplementary emojis and symbols that cause tofu rectangle boxes
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    text = re.sub(r'[\u2600-\u26ff\u2700-\u27bf\u2300-\u23ff]', '', text)
    
    if is_romaji:
        # Fullwidth CJK punctuation to clean ASCII
        trans = {
            '！': '!', '？': '?', '、': ', ', '。': '. ', '・': ' ',
            '〜': '~', '～': '~', '「': '"', '」': '"', '『': '"', '』': '"',
            '（': '(', '）': ')', '［': '[', '］': ']', '　': ' '
        }
        for k, v in trans.items():
            text = text.replace(k, v)
        text = re.sub(r'\b([a-zA-Z]+)Q\b', r'\1!', text)
        text = re.sub(r'\b([a-zA-Z]+)Q([!?]+)', r'\1\2', text)
        text = re.sub(r'([!?,;:])([a-zA-Z])', r'\1 \2', text)
        
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def has_japanese_characters(text: str) -> bool:
    """Check if text contains Hiragana, Katakana, or Kanji."""
    if not text:
        return False
    return bool(re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]', text))

def load_topic_history() -> dict:
    """Load previously generated topics, categories, and vocabulary words."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    data = {"topics": []}
                # Migrate older formats
                if "topics" not in data:
                    data["topics"] = []
                if "used_seeds" not in data:
                    seeds = []
                    for t in data["topics"]:
                        if isinstance(t, dict):
                            if t.get("seed_topic"):
                                seeds.append(t["seed_topic"].lower())
                            elif t.get("title"):
                                seeds.append(t["title"].lower())
                    data["used_seeds"] = seeds
                if "all_taught_words" not in data:
                    words = []
                    for t in data["topics"]:
                        if isinstance(t, dict) and "kanji" in t:
                            words.extend(t["kanji"])
                    data["all_taught_words"] = words
                return data
        except Exception as e:
            print(f"[ContentGen] Warning: Could not parse history.json: {e}")
            return {"topics": [], "used_seeds": [], "all_taught_words": []}
    return {"topics": [], "used_seeds": [], "all_taught_words": []}

def record_topic_in_history(seed_topic: str, lesson: dict, category: str = "General"):
    """Save generated topic and vocabulary words into history to prevent repetition."""
    history = load_topic_history()
    topics_list = history.get("topics", [])
    used_seeds = set(history.get("used_seeds", []))
    all_taught = history.get("all_taught_words", [])

    taught_kanji = [it.get("kanji") for it in lesson.get("items", []) if it.get("kanji")]
    lesson_title = lesson.get("title", seed_topic)

    entry = {
        "seed_topic": seed_topic,
        "title": lesson_title,
        "category": category,
        "kanji": taught_kanji,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    topics_list.append(entry)
    
    if seed_topic:
        used_seeds.add(seed_topic.strip().lower())
    if lesson_title:
        used_seeds.add(lesson_title.strip().lower())
        
    for k in taught_kanji:
        if k and k not in all_taught:
            all_taught.append(k)

    history["topics"] = topics_list
    history["used_seeds"] = list(used_seeds)
    history["all_taught_words"] = all_taught
    history["last_updated"] = entry["date"]
    
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"[ContentGen] Recorded in history: '{seed_topic}' (taught {len(taught_kanji)} words)")
    except Exception as e:
        print(f"[ContentGen] Could not update history: {e}")

def get_next_fresh_category_and_topic() -> tuple:
    """Pick a fresh unique topic across rotating categories that has never been used."""
    history = load_topic_history()
    used_seeds = {s.lower().strip() for s in history.get("used_seeds", []) if isinstance(s, str)}
    
    # Also include legacy titles
    for h in history.get("topics", []):
        if isinstance(h, dict):
            if h.get("seed_topic"):
                used_seeds.add(h["seed_topic"].lower().strip())
            if h.get("title"):
                used_seeds.add(h["title"].lower().strip())
    
    categories = list(CATEGORIZED_TOPICS.keys())
    random.shuffle(categories)
    
    # 1. Look for a completely unused topic
    for cat in categories:
        topics_in_cat = list(CATEGORIZED_TOPICS[cat])
        random.shuffle(topics_in_cat)
        for topic_name, art_prompt in topics_in_cat:
            cleaned_name = topic_name.strip().lower()
            if cleaned_name not in used_seeds:
                return cat, topic_name, art_prompt
                
    # 2. If all 100+ topics were somehow used, find the least recently used one
    print("[ContentGen] Notice: All topic seeds have been used once! Recycling least recently used topic.")
    past_dates = {}
    for h in history.get("topics", []):
        if isinstance(h, dict):
            s = h.get("seed_topic") or h.get("title")
            if s:
                past_dates[s.lower().strip()] = h.get("date", "")
                
    chosen_cat = random.choice(categories)
    topics_in_cat = CATEGORIZED_TOPICS[chosen_cat]
    # Pick the one with oldest date
    sorted_topics = sorted(topics_in_cat, key=lambda t: past_dates.get(t[0].lower().strip(), ""))
    topic_name, art_prompt = sorted_topics[0]
    return chosen_cat, topic_name, art_prompt

def fetch_lesson_from_ai(topic: str = None, item_count: int = DEFAULT_ITEM_COUNT) -> dict:
    """Fetch structured Japanese lesson from Pollinations AI with anti-repetition guardrails."""
    art_prompt = None
    category = "Japanese Lesson"
    seed_topic = topic
    
    if not seed_topic:
        category, seed_topic, art_prompt = get_next_fresh_category_and_topic()
    else:
        art_prompt = f"beautiful {seed_topic} anime aesthetic clean art"

    history = load_topic_history()
    recent_words = history.get("all_taught_words", [])[-50:]
    recent_words_str = ", ".join(recent_words) if recent_words else "None"
    
    prompt = f"""You are a master Japanese teacher for 'Velocity Japanese'.
Create a high-retention 3-item Japanese vocabulary/Kanji lesson for YouTube Shorts & Facebook Reels.
Target Topic: "{seed_topic}"
Count: exactly {item_count} items.

CRITICAL ANTI-DUPLICATION RULE:
Do NOT teach any of these recently taught words: [{recent_words_str}]
Every vocabulary word must be fresh and uniquely relevant to "{seed_topic}".

CRITICAL PRONUNCIATION & TYPOGRAPHY RULES:
- For 'kanji', provide the authentic Japanese word in Kanji/Kana. MUST contain Japanese characters.
- For 'hiragana', provide the EXACT phonetic reading in pure Hiragana (e.g. 'あたま', 'げつようび', 'みず', 'たべる'). This is used for Text-to-Speech pronunciation.
- For 'romaji' and 'example_romaji', use ONLY standard Latin letters and ASCII punctuation (!, ?, .). NEVER use Japanese fullwidth punctuation (like ！？ or 「」) in Romaji.
- Do NOT include emojis in any text fields (kanji, romaji, english, examples).

Requirements:
1. Provide a punchy beginner/intermediate title (no emojis).
2. For each item ({item_count} total):
   - kanji: Japanese word/phrase in Kanji + Kana
   - hiragana: The EXACT phonetic Hiragana reading (crucial for TTS!)
   - romaji: English pronunciation transliteration (clean Latin letters only)
   - english: Clear English meaning (1-3 words)
   - element: Short tag/category (e.g. "Food", "Action", "Travel", "Time")
   - example_ja: Simple, natural Japanese example sentence using the word
   - example_romaji: Clean Latin Romaji with ASCII punctuation (!, ?)
   - example_en: English translation for the example sentence (no emojis)

Return ONLY strictly valid raw JSON format matching this exact schema (no markdown fences, no conversational text):
{{
  "title": "{seed_topic}",
  "category": "{category}",
  "art_prompt": "{art_prompt}",
  "description": "Learn {seed_topic} with Velocity Japanese!",
  "items": [
    {{
      "kanji": "...",
      "hiragana": "...",
      "romaji": "...",
      "english": "...",
      "element": "...",
      "example_ja": "...",
      "example_romaji": "...",
      "example_en": "..."
    }}
  ]
}}"""

    headers = {
        "Content-Type": "application/json"
    }
    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"

    # Try primary model then fallback models (gemini-fast prioritized)
    models_to_try = ["gemini-fast", "openai"]
    if AI_MODEL and AI_MODEL.strip():
        m = AI_MODEL.strip()
        if m in models_to_try:
            models_to_try.remove(m)
        models_to_try.insert(0, m)

    for model_name in models_to_try:
        try:
            print(f"[ContentGen] Requesting lesson from Pollinations AI (model: {model_name})...")
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are a professional Japanese educator. You output ONLY strictly valid JSON for Japanese lessons."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            resp = requests.post(POLLINATIONS_ENDPOINT, json=payload, headers=headers, timeout=35)
            if resp.status_code != 200:
                print(f"[ContentGen] Model {model_name} HTTP {resp.status_code}, trying next...")
                continue
                
            data = resp.json()
            raw_content = data["choices"][0]["message"]["content"].strip()
            
            # Clean markdown fences
            if "```json" in raw_content:
                raw_content = raw_content.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_content:
                raw_content = raw_content.split("```")[1].split("```")[0].strip()
                
            lesson = None
            try:
                lesson = json.loads(raw_content)
            except Exception as parse_err:
                print(f"[ContentGen] Direct JSON parse failed ({parse_err}), attempting regex item recovery for {model_name}...")
                obj_matches = re.findall(r'\{[^{}]*"(?:kanji|Kanji)"[^{}]*\}', raw_content, re.DOTALL)
                if obj_matches:
                    recovered_items = []
                    for om in obj_matches:
                        try:
                            recovered_items.append(json.loads(om))
                        except Exception:
                            continue
                    if recovered_items:
                        lesson = {
                            "title": seed_topic,
                            "category": category,
                            "art_prompt": art_prompt,
                            "items": recovered_items
                        }
                        print(f"[ContentGen] Successfully recovered {len(recovered_items)} items via regex!")
            
            if isinstance(lesson, dict) and "items" in lesson and len(lesson["items"]) > 0:
                cleaned_items = []
                for it in lesson["items"]:
                    k = clean_text(it.get("kanji", ""), is_japanese=True)
                    h = clean_text(it.get("hiragana", ""), is_japanese=True)
                    e = clean_text(it.get("english", ""))
                    if k and e and has_japanese_characters(k):
                        cleaned_items.append({
                            "kanji": k,
                            "hiragana": h or k,
                            "romaji": clean_text(it.get("romaji", ""), is_romaji=True),
                            "english": e,
                            "element": clean_text(it.get("element", "")),
                            "example_ja": clean_text(it.get("example_ja", ""), is_japanese=True),
                            "example_romaji": clean_text(it.get("example_romaji", ""), is_romaji=True),
                            "example_en": clean_text(it.get("example_en", "")),
                        })
                lesson["items"] = cleaned_items[:item_count]
                if len(lesson["items"]) >= 2:
                    lesson["art_prompt"] = lesson.get("art_prompt") or art_prompt
                    lesson["category"] = lesson.get("category") or category
                    record_topic_in_history(seed_topic, lesson, category=lesson["category"])
                    return lesson
        except Exception as e:
            print(f"[ContentGen] Model {model_name} error: {e}. Trying next...")
            continue

    # Fallback if all AI models fail
    print("[ContentGen] AI models unavailable. Selecting next unused curated curriculum topic...")
    for curated in CURATED_TOPICS:
        if seed_topic and seed_topic.lower() in curated["title"].lower():
            res = dict(curated)
            res["items"] = res["items"][:item_count]
            res["art_prompt"] = curated.get("art_prompt") or art_prompt
            record_topic_in_history(seed_topic, res, category=res.get("category", "Curated"))
            return res
            
    chosen = random.choice(CURATED_TOPICS)
    res = dict(chosen)
    res["items"] = res["items"][:item_count]
    res["art_prompt"] = chosen.get("art_prompt") or art_prompt
    record_topic_in_history(res["title"], res, category=res.get("category", "Curated"))
    return res

def get_preset_image_lesson(image_name: str, item_count: int = DEFAULT_ITEM_COUNT) -> dict:
    """Pre-parsed lessons matching the user's inspiration images."""
    if "6075568155066569876" in image_name or "day" in image_name.lower():
        res = dict(CURATED_TOPICS[0])
    elif "6075568155066569877" in image_name or "kanji" in image_name.lower():
        res = dict(CURATED_TOPICS[1])
    else:
        res = dict(CURATED_TOPICS[2])
    res["items"] = res["items"][:item_count]
    return res


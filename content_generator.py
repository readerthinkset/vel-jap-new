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

def clean_text(text: str) -> str:
    """Clean and sanitize text string."""
    if not text:
        return ""
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_topic_history() -> dict:
    """Load previously generated topics and categories."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"topics": [], "categories": []}
    return {"topics": [], "categories": []}

def record_topic_in_history(topic_title: str, category: str = "General"):
    """Save generated topic into history."""
    history = load_topic_history()
    topics_list = history.get("topics", [])
    entry = {
        "title": topic_title,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    topics_list.append(entry)
    history["topics"] = topics_list
    history["last_updated"] = entry["date"]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ContentGen] Could not update history: {e}")

def get_next_fresh_category_and_topic() -> tuple:
    """Pick a fresh unique topic across rotating categories."""
    history = load_topic_history()
    used_titles = {h.get("title", "").lower() for h in history.get("topics", []) if isinstance(h, dict)}
    
    # Try finding an unused topic from categories
    categories = list(CATEGORIZED_TOPICS.keys())
    random.shuffle(categories)
    
    for cat in categories:
        topics_in_cat = CATEGORIZED_TOPICS[cat]
        for topic_name, art_prompt in topics_in_cat:
            if topic_name.lower() not in used_titles:
                return cat, topic_name, art_prompt
                
    # Fallback to random choice if exhausted
    chosen_cat = random.choice(categories)
    topic_name, art_prompt = random.choice(CATEGORIZED_TOPICS[chosen_cat])
    return chosen_cat, topic_name, art_prompt

def fetch_lesson_from_ai(topic: str = None, item_count: int = DEFAULT_ITEM_COUNT) -> dict:
    """Fetch structured Japanese lesson from Pollinations AI."""
    art_prompt = None
    category = "Japanese Lesson"
    
    if not topic:
        category, topic, art_prompt = get_next_fresh_category_and_topic()
    else:
        art_prompt = f"beautiful {topic} anime aesthetic clean art"
    
    prompt = f"""You are a master Japanese teacher for 'Velocity Japanese'.
Create a high-retention 3-item Japanese vocabulary/Kanji lesson for YouTube Shorts & Facebook Reels.
Target Topic: "{topic}"
Count: exactly {item_count} items.

CRITICAL PRONUNCIATION RULE:
- For 'hiragana', provide the EXACT phonetic reading in pure Hiragana (e.g. 'あたま' for 頭, 'げつようび' for 月曜日, 'みず' for 水, 'たべる' for 食べる). This is used for Text-to-Speech pronunciation.

Requirements:
1. Provide a punchy beginner/intermediate title.
2. For each item ({item_count} total):
   - kanji: Japanese word/phrase in Kanji + Kana
   - hiragana: The EXACT phonetic Hiragana reading (crucial for TTS!)
   - romaji: English pronunciation transliteration
   - english: Clear English meaning (1-3 words)
   - element: Short tag/category (e.g. "Food", "Action", "Travel", "Time")
   - example_ja: Simple, natural Japanese example sentence using the word
   - example_romaji: Romaji for the example sentence
   - example_en: English translation for the example sentence

Return ONLY strictly valid raw JSON format matching this exact schema (no markdown fences, no conversational text):
{{
  "title": "{topic}",
  "category": "{category}",
  "art_prompt": "{art_prompt}",
  "description": "Learn {topic} with Velocity Japanese!",
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
        "Authorization": f"Bearer {POLLINATIONS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional Japanese language educator. You output ONLY strictly valid JSON for Japanese lessons."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.75
    }

    try:
        resp = requests.post(POLLINATIONS_ENDPOINT, json=payload, headers=headers, timeout=40)
        resp.raise_for_status()
        data = resp.json()
        raw_content = data["choices"][0]["message"]["content"].strip()
        
        # Clean markdown fences
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1].split("```")[0].strip()
            
        lesson = json.loads(raw_content)
        
        if isinstance(lesson, dict) and "items" in lesson and len(lesson["items"]) > 0:
            cleaned_items = []
            for it in lesson["items"]:
                cleaned_items.append({
                    "kanji": clean_text(it.get("kanji", "")),
                    "hiragana": clean_text(it.get("hiragana", "")),
                    "romaji": clean_text(it.get("romaji", "")),
                    "english": clean_text(it.get("english", "")),
                    "element": clean_text(it.get("element", "")),
                    "example_ja": clean_text(it.get("example_ja", "")),
                    "example_romaji": clean_text(it.get("example_romaji", "")),
                    "example_en": clean_text(it.get("example_en", "")),
                })
            lesson["items"] = [it for it in cleaned_items if it["kanji"] and it["english"]][:item_count]
            if len(lesson["items"]) >= 2:
                lesson["art_prompt"] = lesson.get("art_prompt") or art_prompt
                record_topic_in_history(lesson.get("title", topic), category=lesson.get("category", category))
                return lesson
    except Exception as e:
        print(f"[ContentGen] Pollinations AI Notice: {e}. Using curated curriculum.")

    # Fallback to curated topics trimmed to item_count
    for curated in CURATED_TOPICS:
        if topic and topic.lower() in curated["title"].lower():
            res = dict(curated)
            res["items"] = res["items"][:item_count]
            res["art_prompt"] = curated.get("art_prompt") or art_prompt
            record_topic_in_history(res["title"], category=res.get("category", "Curated"))
            return res
            
    chosen = random.choice(CURATED_TOPICS)
    res = dict(chosen)
    res["items"] = res["items"][:item_count]
    res["art_prompt"] = chosen.get("art_prompt") or art_prompt
    record_topic_in_history(res["title"], category=res.get("category", "Curated"))
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

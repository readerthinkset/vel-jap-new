"""
Velocity Japanese - Social Media Publisher (Facebook & Instagram)
Publishes daily Japanese lessons to Velocity Japanese Facebook Page & Instagram with Pinned Comments.
"""
import os
import sys
import time
import json
from pathlib import Path
from typing import Optional, Dict
import requests

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import WEBSITE_URL, CHANNEL_NAME, BASE_DIR

PAGE_ID = os.getenv("FB_PAGE_ID") or "1048385991689324"
IG_ACCOUNT_ID = os.getenv("IG_ACCOUNT_ID") or "17841422382326051"
TOKEN_CACHE_FILE = BASE_DIR / ".fb_page_token.json"

def get_page_access_token() -> Optional[str]:
    """Retrieve Page Access Token from cache, environment, or Meta User Token."""
    # 1. Environment variables
    direct_tok = os.getenv("FB_PAGE_ACCESS_TOKEN")
    if direct_tok:
        return direct_tok
        
    # 2. Local Cache
    if TOKEN_CACHE_FILE.exists():
        try:
            with open(TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("access_token"):
                    return data["access_token"]
        except Exception:
            pass

    meta_token = os.getenv("META_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")
    if not meta_token:
        print("[Publisher] Notice: No META_ACCESS_TOKEN or FB_PAGE_ACCESS_TOKEN found in environment.")
        return None
        
    # 3. Resolve from Graph API
    url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={meta_token}&limit=100"
    for _ in range(5):
        if not url:
            break
        try:
            res = requests.get(url, timeout=12).json()
            for p in res.get("data", []):
                if p.get("id") == PAGE_ID or "japanese" in p.get("name", "").lower():
                    tok = p.get("access_token")
                    try:
                        with open(TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
                            json.dump({"access_token": tok, "page_id": PAGE_ID, "name": p.get("name")}, f)
                    except Exception:
                        pass
                    return tok
            url = res.get("paging", {}).get("next")
        except Exception as e:
            print(f"[Publisher] Error fetching accounts: {e}")
            break
    return None

def generate_pinned_comment(lesson: dict) -> str:
    """Generate structured pinned comment with lesson breakdown and website link."""
    title = lesson.get("title", "Daily Lesson")
    items = lesson.get("items", [])
    
    lines = [
        f"🌸 Velocity Japanese Lesson Recap: {title}",
        "━━━━━━━━━━━━━━━━━━━━━",
        "📝 Vocabulary & Kanji Breakdown:"
    ]
    for i, it in enumerate(items, 1):
        k = it.get("kanji", "")
        h = it.get("hiragana", "")
        r = it.get("romaji", "")
        e = it.get("english", "")
        ex_ja = it.get("example_ja", "")
        ex_en = it.get("example_en", "")
        lines.append(f"{i}. {k} 【{h}】 ({r}) — {e}")
        if ex_ja:
            lines.append(f"   💬 例文: {ex_ja} (\"{ex_en}\")")
            
    lines.extend([
        "━━━━━━━━━━━━━━━━━━━━━",
        f"🌐 Free PDF Vocabulary Guides & Lessons: https://{WEBSITE_URL}",
        "🇯🇵 Follow @VelocityJapanese for daily lessons!",
        "💬 Which word was new for you today? Comment below! 👇"
    ])
    return "\n".join(lines)

def publish_to_facebook(
    video_path: Path,
    lesson: dict,
    page_token: Optional[str] = None
) -> Optional[dict]:
    """Upload video reel to Facebook Page and add pinned first comment."""
    if not page_token:
        page_token = get_page_access_token()
        
    if not page_token:
        print("[Publisher] Cannot publish to Facebook: missing Page Access Token.")
        return None
        
    if not video_path.exists():
        print(f"[Publisher] Video file does not exist: {video_path}")
        return None

    print(f"\n[Facebook Publisher] Uploading '{video_path.name}' to Velocity Japanese (Page ID: {PAGE_ID})...")
    
    title = f"🇯🇵 {lesson.get('title', 'Daily Japanese Lesson')} | Velocity Japanese"
    items = lesson.get("items", [])
    
    desc_lines = [
        title,
        "",
        "Learn essential Japanese vocabulary, natural pronunciation, and practical example sentences!",
        "",
        "📚 In This Video:"
    ]
    for i, it in enumerate(items, 1):
        desc_lines.append(f"  {i}. {it.get('kanji')} 【{it.get('hiragana')}】: {it.get('english')}")
        
    desc_lines.extend([
        "",
        f"🌐 Full Guides & PDFs: https://{WEBSITE_URL}",
        "🔔 Follow Velocity Japanese for daily lessons!",
        "#VelocityJapanese #LearnJapanese #JapaneseLesson #JLPT #JLPTN5 #Nihongo #Reels #Shorts"
    ])
    description = "\n".join(desc_lines)
    
    upload_url = f"https://graph-video.facebook.com/v19.0/{PAGE_ID}/videos"
    data = {
        "title": title,
        "description": description,
        "access_token": page_token
    }
    
    try:
        with open(video_path, "rb") as video_file:
            files = {"source": video_file}
            resp = requests.post(upload_url, data=data, files=files, timeout=300)
            
        res_json = resp.json()
        if "id" in res_json:
            video_id = res_json["id"]
            print(f"✅ Video published successfully! Facebook Video ID: {video_id}")
            
            # Post Pinned First Comment
            time.sleep(3)
            pinned_comment_text = generate_pinned_comment(lesson)
            comment_url = f"https://graph.facebook.com/v19.0/{video_id}/comments"
            comment_data = {
                "message": pinned_comment_text,
                "access_token": page_token
            }
            c_resp = requests.post(comment_url, data=comment_data, timeout=30)
            c_json = c_resp.json()
            if "id" in c_json:
                print(f"💬 Pinned first comment posted! Comment ID: {c_json['id']}")
            else:
                print(f"💬 Notice on comment: {c_json}")
                
            return {
                "platform": "facebook",
                "video_id": video_id,
                "status": "published",
                "page_id": PAGE_ID
            }
        else:
            print(f"❌ Facebook upload error: {res_json}")
            return None
    except Exception as e:
        print(f"❌ Exception during Facebook upload: {e}")
        return None

if __name__ == "__main__":
    print("Testing Facebook Page Connection...")
    tok = get_page_access_token()
    if tok:
        print(f"Successfully retrieved Velocity Japanese Token: {tok[:20]}...")
    else:
        print("Could not retrieve Page Token.")

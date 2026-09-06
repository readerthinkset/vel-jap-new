"""
Velocity Japanese - Visual Card & Graphic Renderer (V3 - Scenario Art & Website Branding)
Renders high-contrast, visually stunning Japanese infographic cards with backdrop artwork.
"""
import math
import os
import sys
import urllib.parse
from pathlib import Path
from typing import Tuple, List, Optional
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

from config import (
    FONTS_DIR,
    VERTICAL_WIDTH,
    VERTICAL_HEIGHT,
    HORIZONTAL_WIDTH,
    HORIZONTAL_HEIGHT,
    DARK_BG,
    CARD_BG,
    CARD_BORDER,
    CARD_INNER_BG,
    ACCENT_RED,
    ACCENT_GOLD,
    ACCENT_CYAN,
    ACCENT_SAKURA,
    WHITE,
    TEXT_MUTED,
    TEXT_EXAMPLE_EN,
    DARK_LINE,
    CHANNEL_NAME,
    WEBSITE_URL,
    TAGLINE,
    CTA_TEXT,
    FOOTER_TAG,
    POLLINATIONS_API_KEY
)

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def get_font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    """Load Latin / English font."""
    candidates = []
    if italic and bold:
        candidates.extend([
            FONTS_DIR / "DejaVuSans-BoldOblique.ttf",
            "C:/Windows/Fonts/segoeuiz.ttf",
            "C:/Windows/Fonts/arialbi.ttf"
        ])
    elif italic:
        candidates.extend([
            FONTS_DIR / "DejaVuSans-Oblique.ttf",
            "C:/Windows/Fonts/segoeuii.ttf",
            "C:/Windows/Fonts/ariali.ttf"
        ])
    elif bold:
        candidates.extend([
            FONTS_DIR / "DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf"
        ])
    else:
        candidates.extend([
            FONTS_DIR / "DejaVuSans.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf"
        ])

    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_japanese_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    """Load Japanese font supporting Kanji, Hiragana, Katakana."""
    candidates = []
    if bold:
        candidates.extend([
            FONTS_DIR / "NotoSansJP-Bold.ttf",
            "C:/Windows/Fonts/YuGothB.ttc",
            "C:/Windows/Fonts/meiryob.ttc",
            "C:/Windows/Fonts/msgothic.ttc"
        ])
    else:
        candidates.extend([
            FONTS_DIR / "NotoSansJP-Regular.ttf",
            "C:/Windows/Fonts/YuGothM.ttc",
            "C:/Windows/Fonts/meiryo.ttc",
            "C:/Windows/Fonts/msgothic.ttc"
        ])

    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                continue
    return get_font(size, bold=bold)

def fetch_scenario_background(prompt: str, cache_path: Path, width: int = VERTICAL_WIDTH, height: int = VERTICAL_HEIGHT) -> Optional[Image.Image]:
    """Fetch themed scenario backdrop from Pollinations image API or load from cache."""
    if cache_path.exists():
        try:
            return Image.open(cache_path).convert("RGB")
        except Exception:
            pass
            
    if not prompt:
        prompt = "mount fuji cherry blossoms spring kyoto temple aesthetic anime art"
        
    encoded = urllib.parse.quote(f"{prompt} high quality cinematic clean anime illustration")
    # Fetch 720x1280 and scale up to 1080x1920
    fetch_w = 720 if width < height else 1280
    fetch_h = 1280 if width < height else 720
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={fetch_w}&height={fetch_h}&nologo=true"
    
    headers = {"User-Agent": "VelocityJapaneseBot/1.0"}
    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
        
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, "wb") as f:
                f.write(r.content)
            img = Image.open(cache_path).convert("RGB")
            return img.resize((width, height), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"[Renderer] Notice: Background art fetch skipped ({e}). Using sleek dark theme.")
    return None

def create_base_canvas(width: int, height: int, bg_img: Optional[Image.Image] = None) -> Image.Image:
    """Create rich dark glass canvas with optional dimmed backdrop."""
    canvas = Image.new("RGB", (width, height), DARK_BG)
    if bg_img:
        resized_bg = bg_img.resize((width, height), Image.Resampling.LANCZOS)
        # Apply slight blur and darken for readability
        blurred_bg = resized_bg.filter(ImageFilter.GaussianBlur(radius=8))
        enhancer = ImageEnhance.Brightness(blurred_bg)
        dimmed_bg = enhancer.enhance(0.28) # 28% brightness for deep high contrast
        canvas.paste(dimmed_bg, (0, 0))
        
    # Ambient color glows
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([(width // 2 - 450, 250), (width // 2 + 450, 850)], fill=(70, 180, 255, 22))
    gdraw.ellipse([(width // 2 - 400, 1100), (width // 2 + 400, 1650)], fill=(255, 60, 85, 20))
    canvas.paste(glow, (0, 0), glow)
    return canvas

def draw_japanese_flag(img: Image.Image, center_x: int, center_y: int, radius: int = 24):
    """Draw circular Japanese Hinomaru flag badge."""
    flag_img = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(flag_img)
    fdraw.rectangle([(0, 0), (radius * 2, radius * 2)], fill=(255, 255, 255, 255))
    fdraw.ellipse(
        [(int(radius * 0.45), int(radius * 0.45)), (int(radius * 1.55), int(radius * 1.55))],
        fill=(188, 0, 45, 255)
    )
    mask = Image.new("L", (radius * 2, radius * 2), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([0, 0, radius * 2, radius * 2], fill=255)
    img.paste(flag_img, (center_x - radius, center_y - radius), mask)

def draw_torii_icon(draw: ImageDraw.ImageDraw, x: int, y: int, color: Tuple[int, int, int] = ACCENT_RED, scale: float = 1.0):
    """Draw stylized Japanese Torii gate icon."""
    draw.rounded_rectangle([x - int(28 * scale), y - int(14 * scale), x + int(28 * scale), y - int(8 * scale)], radius=int(2*scale), fill=color)
    draw.rectangle([x - int(24 * scale), y - int(4 * scale), x + int(24 * scale), y - int(0 * scale)], fill=color)
    draw.rectangle([x - int(16 * scale), y - int(6 * scale), x - int(11 * scale), y + int(22 * scale)], fill=color)
    draw.rectangle([x + int(11 * scale), y - int(6 * scale), x + int(16 * scale), y + int(22 * scale)], fill=color)
    draw.rectangle([x - int(3 * scale), y - int(8 * scale), x + int(3 * scale), y - int(4 * scale)], fill=color)

def draw_header(img: Image.Image, draw: ImageDraw.ImageDraw, width: int, is_vertical: bool = True):
    """Render top header bar with branding and website."""
    header_y = 75 if is_vertical else 55
    torii_x = 70 if is_vertical else 80
    draw_torii_icon(draw, torii_x, header_y, color=ACCENT_RED, scale=1.3 if is_vertical else 1.1)
    
    f_brand_main = get_font(34 if is_vertical else 28, bold=True)
    f_sub = get_japanese_font(18 if is_vertical else 16, bold=False)
    
    text_x = torii_x + 50
    draw.text((text_x, header_y - 12), "VELOCITY", fill=WHITE, font=f_brand_main, anchor="lm")
    bbox1 = draw.textbbox((text_x, header_y - 12), "VELOCITY", font=f_brand_main, anchor="lm")
    
    draw.text((bbox1[2] + 8, header_y - 12), "JAPANESE", fill=ACCENT_RED, font=f_brand_main, anchor="lm")
    bbox2 = draw.textbbox((bbox1[2] + 8, header_y - 12), "JAPANESE", font=f_brand_main, anchor="lm")
    
    # Official Website Subtitle
    draw.text((text_x, header_y + 18), f"{WEBSITE_URL} • 日本語", fill=TEXT_MUTED, font=f_sub, anchor="lm")
    
    flag_x = width - 70 if is_vertical else width - 80
    draw_japanese_flag(img, flag_x, header_y, radius=24 if is_vertical else 20)
    
    sep_y = 135 if is_vertical else 105
    draw.line([(40, sep_y), (width - 40, sep_y)], fill=DARK_LINE, width=2)
    draw.line([(width // 2 - 50, sep_y), (width // 2 + 50, sep_y)], fill=ACCENT_RED, width=4)

def draw_footer(draw: ImageDraw.ImageDraw, width: int, height: int, progress: float = 0.0, is_vertical: bool = True):
    """Render footer with branding and video progress bar."""
    footer_y = height - 75 if is_vertical else height - 55
    
    f_footer_bold = get_font(22 if is_vertical else 18, bold=True)
    f_footer_sub = get_font(17 if is_vertical else 14, bold=False)
    
    sep_y = height - 120 if is_vertical else height - 85
    draw.line([(40, sep_y), (width - 40, sep_y)], fill=DARK_LINE, width=2)
    
    draw.text((width // 2, footer_y - 10), f"Visit {WEBSITE_URL} for Free Japanese PDFs", fill=WHITE, font=f_footer_bold, anchor="mm")
    draw.text((width // 2, footer_y + 18), "Follow @VelocityJapanese • Facebook & YouTube", fill=TEXT_MUTED, font=f_footer_sub, anchor="mm")
    
    # Bottom Progress Bar
    bar_height = 8 if is_vertical else 6
    draw.rectangle([(0, height - bar_height), (width, height)], fill=(25, 30, 42))
    fill_w = int(width * min(1.0, max(0.0, progress)))
    if fill_w > 0:
        draw.rectangle([(0, height - bar_height), (fill_w, height)], fill=ACCENT_RED)

def wrap_japanese_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> List[str]:
    """
    Wrap Japanese character-by-character so no text is EVER cropped on the left or right edges!
    """
    if not text:
        return []
    lines = []
    cur_line = ""
    for ch in text:
        test = cur_line + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            cur_line = test
        else:
            if cur_line:
                lines.append(cur_line)
            cur_line = ch
    if cur_line:
        lines.append(cur_line)
    return lines

def wrap_english_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> List[str]:
    """Wrap English text word-by-word safely."""
    if not text:
        return []
    words = text.split()
    lines = []
    cur = []
    for w in words:
        test = " ".join(cur + [w])
        bb = draw.textbbox((0, 0), test, font=font)
        if (bb[2] - bb[0]) <= max_w or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines

def render_item_frame(
    item: dict,
    index: int,
    total: int,
    width: int = VERTICAL_WIDTH,
    height: int = VERTICAL_HEIGHT,
    progress: float = 0.0,
    bg_img: Optional[Image.Image] = None,
    category: Optional[str] = None
) -> Image.Image:
    """
    Render high-retention Japanese flashcard with hero scenario artwork,
    crisp Kanji typography, furigana readings, and structured example sentence.
    """
    is_vertical = height > width
    
    # 1. Base Canvas with subtle ambient blur of the artwork
    canvas = Image.new("RGB", (width, height), (10, 12, 20))
    if bg_img:
        backdrop = bg_img.resize((width, height), Image.Resampling.LANCZOS)
        backdrop_blurred = backdrop.filter(ImageFilter.GaussianBlur(radius=25))
        backdrop_dim = ImageEnhance.Brightness(backdrop_blurred).enhance(0.35)
        canvas.paste(backdrop_dim, (0, 0))
        
    # Top and bottom dark vignettes for header/footer readability
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for y in range(160):
        alpha = int(220 * (1 - y / 160))
        vdraw.line([(0, y), (width, y)], fill=(8, 10, 16, alpha))
    for y in range(height - 140, height):
        alpha = int(240 * ((y - (height - 140)) / 140))
        vdraw.line([(0, y), (width, y)], fill=(8, 10, 16, alpha))
    canvas.paste(vignette, (0, 0), vignette)

    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, width, is_vertical=is_vertical)

    cat_label = (category or item.get("category") or item.get("element") or "JAPANESE").upper()

    if is_vertical:
        # === VERTICAL 9:16 (Shorts / Reels / TikTok) ===
        art_mx = 45
        art_top = 135
        art_h = 520
        art_w = width - (art_mx * 2)
        art_bot = art_top + art_h
        
        # 1. Hero Artwork Display
        if bg_img:
            bw, bh = bg_img.size
            target_ratio = art_w / art_h
            current_ratio = bw / bh
            if current_ratio > target_ratio:
                new_w = int(bh * target_ratio)
                crop_x = (bw - new_w) // 2
                cropped_art = bg_img.crop((crop_x, 0, crop_x + new_w, bh))
            else:
                new_h = int(bw / target_ratio)
                crop_y = max(0, min(bh - new_h, int((bh - new_h) * 0.4)))
                cropped_art = bg_img.crop((0, crop_y, bw, crop_y + new_h))
                
            cropped_art = cropped_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
            
            mask = Image.new("L", (art_w, art_h), 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.rounded_rectangle([(0, 0), (art_w, art_h)], radius=26, fill=255)
            canvas.paste(cropped_art, (art_mx, art_top), mask)
            
            # Subtle gradient overlay
            art_overlay = Image.new("RGBA", (art_w, art_h), (0, 0, 0, 0))
            adraw = ImageDraw.Draw(art_overlay)
            for y in range(art_h - 120, art_h):
                a = int(180 * ((y - (art_h - 120)) / 120))
                adraw.line([(0, y), (art_w, y)], fill=(10, 14, 24, a))
            for y in range(0, 70):
                a = int(130 * (1 - y / 70))
                adraw.line([(0, y), (art_w, y)], fill=(10, 14, 24, a))
            canvas.paste(art_overlay, (art_mx, art_top), art_overlay)
            
            draw.rounded_rectangle([(art_mx, art_top), (width - art_mx, art_bot)], radius=26, outline=(255, 75, 100), width=3)
            
        # Category Tag Pill (Top Left)
        f_badge_cat = get_font(18, bold=True)
        c_bbox = draw.textbbox((0, 0), cat_label, font=f_badge_cat)
        cw = max(160, (c_bbox[2] - c_bbox[0]) + 36)
        draw.rounded_rectangle([(art_mx + 20, art_top + 20), (art_mx + 20 + cw, art_top + 60)], radius=14, fill=(12, 16, 26, 230), outline=(70, 180, 255), width=2)
        draw.text((art_mx + 20 + cw // 2, art_top + 40), cat_label, fill=ACCENT_CYAN, font=f_badge_cat, anchor="mm")
        
        # Counter Badge Pill (Top Right)
        counter_str = f"WORD {index:02d} / {total:02d}"
        f_badge_cnt = get_font(18, bold=True)
        cnt_w = 170
        draw.rounded_rectangle([(width - art_mx - 20 - cnt_w, art_top + 20), (width - art_mx - 20, art_top + 60)], radius=14, fill=(255, 60, 85, 230))
        draw.text((width - art_mx - 20 - cnt_w // 2, art_top + 40), counter_str, fill=WHITE, font=f_badge_cnt, anchor="mm")

        # 2. Vocabulary Card (Middle Section)
        card_mx = 45
        card_top = 680
        card_h = 510
        card_bot = card_top + card_h
        
        glass_card = Image.new("RGBA", (width - card_mx * 2, card_h), (16, 22, 34, 235))
        gdraw = ImageDraw.Draw(glass_card)
        gdraw.rounded_rectangle([(0, 0), (width - card_mx * 2, card_h)], radius=26, outline=(65, 80, 110), width=2)
        canvas.paste(glass_card, (card_mx, card_top), glass_card)
        draw.line([(card_mx + 80, card_top + 2), (width - card_mx - 80, card_top + 2)], fill=ACCENT_RED, width=3)
        
        kanji_text = item.get("kanji", "")
        hiragana_text = item.get("hiragana", "")
        romaji_text = item.get("romaji", "")
        english_text = item.get("english", "").upper()
        
        k_len = len(kanji_text)
        k_size = 150 if k_len <= 2 else (120 if k_len <= 4 else 90)
        f_kanji = get_japanese_font(k_size, bold=True)
        kanji_y = card_top + 120
        
        # Kanji Glow Shadow
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-3, 3), (3, 3)]:
            draw.text((width // 2 + dx, kanji_y + dy), kanji_text, fill=(255, 60, 85, 100), font=f_kanji, anchor="mm")
        draw.text((width // 2, kanji_y), kanji_text, fill=WHITE, font=f_kanji, anchor="mm")
        
        f_hira = get_japanese_font(46, bold=True)
        hira_y = kanji_y + (k_size // 2) + 40
        draw.text((width // 2, hira_y), f"【 {hiragana_text} 】", fill=ACCENT_SAKURA, font=f_hira, anchor="mm")
        
        f_rom = get_font(34, italic=True)
        rom_y = hira_y + 52
        draw.text((width // 2, rom_y), romaji_text, fill=TEXT_MUTED, font=f_rom, anchor="mm")
        
        f_eng = get_font(44, bold=True)
        eng_bbox = draw.textbbox((0, 0), english_text, font=f_eng)
        eng_w = max(440, (eng_bbox[2] - eng_bbox[0]) + 100)
        eng_h = 76
        eng_x1 = width // 2 - eng_w // 2
        eng_y1 = rom_y + 36
        draw.rounded_rectangle([(eng_x1 - 2, eng_y1 - 2), (eng_x1 + eng_w + 2, eng_y1 + eng_h + 2)], radius=20, fill=(255, 204, 0, 60))
        draw.rounded_rectangle([(eng_x1, eng_y1), (eng_x1 + eng_w, eng_y1 + eng_h)], radius=18, fill=(28, 22, 10), outline=ACCENT_GOLD, width=3)
        draw.text((width // 2, eng_y1 + eng_h // 2), english_text, fill=ACCENT_GOLD, font=f_eng, anchor="mm")

        # 3. Practical Example Sentence Card (Bottom Section)
        ex_top = 1215
        ex_h = 565
        glass_ex = Image.new("RGBA", (width - card_mx * 2, ex_h), (12, 17, 27, 240))
        gex_draw = ImageDraw.Draw(glass_ex)
        gex_draw.rounded_rectangle([(0, 0), (width - card_mx * 2, ex_h)], radius=26, outline=(55, 70, 100), width=2)
        canvas.paste(glass_ex, (card_mx, ex_top), glass_ex)
        
        tag_str = "例文 • PRACTICAL EXAMPLE"
        f_tag = get_japanese_font(18, bold=True)
        t_bbox = draw.textbbox((0, 0), tag_str, font=f_tag)
        t_w = (t_bbox[2] - t_bbox[0]) + 36
        draw.rounded_rectangle([(card_mx + 25, ex_top + 20), (card_mx + 25 + t_w, ex_top + 62)], radius=14, fill=(22, 32, 48), outline=(70, 180, 255), width=1)
        draw.text((card_mx + 25 + t_w // 2, ex_top + 41), tag_str, fill=ACCENT_CYAN, font=f_tag, anchor="mm")
        
        max_w = width - (card_mx + 45) * 2
        example_ja = item.get("example_ja", "")
        example_romaji = item.get("example_romaji", "")
        example_en = item.get("example_en", "")
        
        f_ex_ja = get_japanese_font(48, bold=True)
        ja_lines = wrap_japanese_text(draw, example_ja, f_ex_ja, max_w=max_w)
        
        f_ex_rom = get_font(32, italic=True)
        rom_lines = wrap_english_text(draw, example_romaji, f_ex_rom, max_w=max_w) if example_romaji else []
        
        f_ex_en = get_font(38, bold=True)
        en_lines = wrap_english_text(draw, f'"{example_en}"', f_ex_en, max_w=max_w) if example_en else []
        
        total_text_h = (len(ja_lines) * 64) + (len(rom_lines) * 44) + (len(en_lines) * 52) + 60
        start_y = ex_top + 80 + max(20, (ex_h - 100 - total_text_h) // 2)
        
        curr_y = start_y
        for jl in ja_lines:
            draw.text((width // 2, curr_y), jl, fill=WHITE, font=f_ex_ja, anchor="mm")
            curr_y += 64
        curr_y += 12
        for rl in rom_lines:
            draw.text((width // 2, curr_y), rl, fill=TEXT_MUTED, font=f_ex_rom, anchor="mm")
            curr_y += 44
        curr_y += 16
        for el in en_lines:
            draw.text((width // 2, curr_y), el, fill=TEXT_EXAMPLE_EN, font=f_ex_en, anchor="mm")
            curr_y += 52

    else:
        # === HORIZONTAL 16:9 (YouTube Desktop / Standard) ===
        # Split screen: Left = Artwork Hero, Right = Vocab & Example Cards
        left_w = int(width * 0.44)
        right_w = width - left_w - 90
        art_top = 120
        art_h = height - 210
        
        if bg_img:
            bw, bh = bg_img.size
            crop_art = bg_img.resize((left_w, art_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (left_w, art_h), 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.rounded_rectangle([(0, 0), (left_w, art_h)], radius=24, fill=255)
            canvas.paste(crop_art, (45, art_top), mask)
            draw.rounded_rectangle([(45, art_top), (45 + left_w, art_top + art_h)], radius=24, outline=(255, 75, 100), width=3)
            
        # Left side badge
        f_badge_cnt = get_font(20, bold=True)
        draw.rounded_rectangle([(65, art_top + 20), (240, art_top + 64)], radius=14, fill=(255, 60, 85, 230))
        draw.text((152, art_top + 42), f"WORD {index:02d} / {total:02d}", fill=WHITE, font=f_badge_cnt, anchor="mm")
        
        # Right Side Vocab Card (Top)
        rc_x = 45 + left_w + 30
        vc_top = art_top
        vc_h = int(art_h * 0.48)
        draw.rounded_rectangle([(rc_x, vc_top), (rc_x + right_w, vc_top + vc_h)], radius=22, fill=(16, 22, 34, 235), outline=(65, 80, 110), width=2)
        
        kanji_text = item.get("kanji", "")
        hiragana_text = item.get("hiragana", "")
        english_text = item.get("english", "").upper()
        
        f_kanji = get_japanese_font(100, bold=True)
        f_hira = get_japanese_font(36, bold=True)
        f_eng = get_font(34, bold=True)
        
        mid_x = rc_x + right_w // 2
        draw.text((mid_x, vc_top + 70), kanji_text, fill=WHITE, font=f_kanji, anchor="mm")
        draw.text((mid_x, vc_top + 135), f"【 {hiragana_text} 】", fill=ACCENT_SAKURA, font=f_hira, anchor="mm")
        draw.rounded_rectangle([(mid_x - 180, vc_top + 160), (mid_x + 180, vc_top + 210)], radius=14, fill=(28, 22, 10), outline=ACCENT_GOLD, width=2)
        draw.text((mid_x, vc_top + 185), english_text, fill=ACCENT_GOLD, font=f_eng, anchor="mm")
        
        # Right Side Example Card (Bottom)
        ec_top = vc_top + vc_h + 20
        ec_h = art_h - vc_h - 20
        draw.rounded_rectangle([(rc_x, ec_top), (rc_x + right_w, ec_top + ec_h)], radius=22, fill=(12, 17, 27, 240), outline=(55, 70, 100), width=2)
        
        example_ja = item.get("example_ja", "")
        example_en = item.get("example_en", "")
        f_ex_ja = get_japanese_font(34, bold=True)
        f_ex_en = get_font(28, bold=True)
        
        draw.text((mid_x, ec_top + 55), example_ja, fill=WHITE, font=f_ex_ja, anchor="mm")
        draw.text((mid_x, ec_top + 115), f'"{example_en}"', fill=TEXT_EXAMPLE_EN, font=f_ex_en, anchor="mm")

    draw_footer(draw, width, height, progress=progress, is_vertical=is_vertical)
    return canvas

def render_outro_frame(
    title: str,
    width: int = VERTICAL_WIDTH,
    height: int = VERTICAL_HEIGHT,
    progress: float = 1.0,
    bg_img: Optional[Image.Image] = None
) -> Image.Image:
    """Render the concluding CTA card with celebratory artwork and website sync."""
    is_vertical = height > width
    
    canvas = Image.new("RGB", (width, height), (10, 12, 20))
    if bg_img:
        backdrop = bg_img.resize((width, height), Image.Resampling.LANCZOS)
        backdrop_blurred = backdrop.filter(ImageFilter.GaussianBlur(radius=25))
        backdrop_dim = ImageEnhance.Brightness(backdrop_blurred).enhance(0.35)
        canvas.paste(backdrop_dim, (0, 0))
        
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for y in range(160):
        alpha = int(220 * (1 - y / 160))
        vdraw.line([(0, y), (width, y)], fill=(8, 10, 16, alpha))
    for y in range(height - 140, height):
        alpha = int(240 * ((y - (height - 140)) / 140))
        vdraw.line([(0, y), (width, y)], fill=(8, 10, 16, alpha))
    canvas.paste(vignette, (0, 0), vignette)

    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, width, is_vertical=is_vertical)

    art_mx = 45 if is_vertical else 140
    art_top = 135 if is_vertical else 120
    art_h = 500 if is_vertical else 380
    art_w = width - (art_mx * 2)
    art_bot = art_top + art_h

    # 1. Hero Artwork Display with Celebratory Badge
    if bg_img:
        bw, bh = bg_img.size
        target_ratio = art_w / art_h
        current_ratio = bw / bh
        if current_ratio > target_ratio:
            new_w = int(bh * target_ratio)
            crop_x = (bw - new_w) // 2
            cropped_art = bg_img.crop((crop_x, 0, crop_x + new_w, bh))
        else:
            new_h = int(bw / target_ratio)
            crop_y = max(0, min(bh - new_h, int((bh - new_h) * 0.4)))
            cropped_art = bg_img.crop((0, crop_y, bw, crop_y + new_h))
            
        cropped_art = cropped_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
        mask = Image.new("L", (art_w, art_h), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([(0, 0), (art_w, art_h)], radius=26, fill=255)
        canvas.paste(cropped_art, (art_mx, art_top), mask)
        draw.rounded_rectangle([(art_mx, art_top), (width - art_mx, art_bot)], radius=26, outline=ACCENT_GOLD, width=3)
        
    # Congratulations Banner Pill
    f_badge = get_font(20, bold=True)
    draw.rounded_rectangle([(width // 2 - 160, art_top + 20), (width // 2 + 160, art_top + 64)], radius=14, fill=(255, 60, 85, 230))
    draw.text((width // 2, art_top + 42), "LESSON COMPLETE 🎉", fill=WHITE, font=f_badge, anchor="mm")

    # 2. Main Outro Card
    card_top = art_bot + 35
    card_h = height - card_top - 140
    glass_card = Image.new("RGBA", (width - art_mx * 2, card_h), (16, 22, 34, 235))
    gdraw = ImageDraw.Draw(glass_card)
    gdraw.rounded_rectangle([(0, 0), (width - art_mx * 2, card_h)], radius=26, outline=(65, 80, 110), width=2)
    canvas.paste(glass_card, (art_mx, card_top), glass_card)

    f_cta_main = get_font(54 if is_vertical else 42, bold=True)
    f_ja_bye = get_japanese_font(64 if is_vertical else 48, bold=True)
    f_sub = get_font(30 if is_vertical else 24, bold=False)

    draw.text((width // 2, card_top + 80), "Great Job!", fill=ACCENT_GOLD, font=f_cta_main, anchor="mm")
    draw.text((width // 2, card_top + 165), "お疲れ様でした！", fill=WHITE, font=f_ja_bye, anchor="mm")
    draw.text((width // 2, card_top + 245), "You completed today's lesson!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    # Website Link Box
    box_y = card_top + 310
    box_h = 240 if is_vertical else 180
    draw.rounded_rectangle([(art_mx + 35, box_y), (width - art_mx - 35, box_y + box_h)], radius=22, fill=(12, 16, 26), outline=ACCENT_RED, width=3)
    
    f_brand_big = get_font(38 if is_vertical else 30, bold=True)
    f_site_url = get_font(32 if is_vertical else 24, bold=True)
    f_sub_gold = get_font(26 if is_vertical else 20, bold=False)
    f_bye = get_japanese_font(28 if is_vertical else 22, bold=True)

    draw.text((width // 2, box_y + 45), "Follow Velocity Japanese", fill=WHITE, font=f_brand_big, anchor="mm")
    draw.rounded_rectangle([(width // 2 - 250, box_y + 82), (width // 2 + 250, box_y + 138)], radius=14, fill=ACCENT_RED)
    draw.text((width // 2, box_y + 110), WEBSITE_URL, fill=WHITE, font=f_site_url, anchor="mm")
    draw.text((width // 2, box_y + 165), "Free Japanese Lessons & PDFs", fill=ACCENT_GOLD, font=f_sub_gold, anchor="mm")
    draw.text((width // 2, box_y + 208), "また明日！ • See you tomorrow!", fill=TEXT_MUTED, font=f_bye, anchor="mm")

    draw_footer(draw, width, height, progress=progress, is_vertical=is_vertical)
    return canvas

def render_thumbnail(lesson: dict, width: int = VERTICAL_WIDTH, height: int = VERTICAL_HEIGHT, bg_img: Optional[Image.Image] = None) -> Image.Image:
    """Render eye-catching video thumbnail."""
    items = lesson.get("items", [])
    cat = lesson.get("category", "Japanese")
    if items:
        return render_item_frame(items[0], 1, len(items), width, height, progress=0.0, bg_img=bg_img, category=cat)
    return render_outro_frame(lesson.get("title", "Japanese Lesson"), width, height, progress=0.0, bg_img=bg_img)


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
    FOOTER_TAG
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
    
    try:
        r = requests.get(url, timeout=25)
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
    bg_img: Optional[Image.Image] = None
) -> Image.Image:
    """
    Render flashcard with massive, clear typography and prominent example sentence.
    Zero left/right cropping guaranteed.
    """
    is_vertical = height > width
    img = create_base_canvas(width, height, bg_img)
    draw = ImageDraw.Draw(img)
    
    draw_header(img, draw, width, is_vertical=is_vertical)
    
    card_mx = 45 if is_vertical else 140
    card_top = 155 if is_vertical else 120
    card_bot = height - 135 if is_vertical else height - 95
    
    # Outer Main Card (Semi-transparent dark glass)
    draw.rounded_rectangle([(card_mx, card_top), (width - card_mx, card_bot)], radius=24, fill=(18, 24, 38), outline=CARD_BORDER, width=2)
    
    # 1. Top Card Bar: Counter Badge & Category/Element
    top_bar_y = card_top + 36
    counter_str = f"WORD {index:02d} / {total:02d}"
    draw.rounded_rectangle([(card_mx + 25, top_bar_y - 18), (card_mx + 185, top_bar_y + 18)], radius=12, fill=ACCENT_RED)
    f_badge = get_font(18, bold=True)
    draw.text((card_mx + 105, top_bar_y), counter_str, fill=WHITE, font=f_badge, anchor="mm")
    
    element_text = item.get("element", "")
    if element_text:
        f_elem = get_japanese_font(22, bold=True)
        draw.text((width - card_mx - 35, top_bar_y), element_text, fill=ACCENT_GOLD, font=f_elem, anchor="rm")
        
    div1_y = card_top + 72
    draw.line([(card_mx + 20, div1_y), (width - card_mx - 20, div1_y)], fill=DARK_LINE, width=2)
    
    # 2. Main Kanji Character (EXTRA LARGE & CRISP)
    kanji_text = item.get("kanji", "")
    hiragana_text = item.get("hiragana", "")
    romaji_text = item.get("romaji", "")
    english_text = item.get("english", "")
    
    k_len = len(kanji_text)
    if k_len <= 2:
        k_size = 160 if is_vertical else 110
    elif k_len <= 4:
        k_size = 130 if is_vertical else 90
    elif k_len <= 7:
        k_size = 95 if is_vertical else 70
    else:
        k_size = 72 if is_vertical else 54
        
    f_kanji = get_japanese_font(k_size, bold=True)
    kanji_y = card_top + (215 if is_vertical else 155)
    
    # Kanji Shadow & Main Text
    draw.text((width // 2 + 3, kanji_y + 4), kanji_text, fill=(8, 12, 18), font=f_kanji, anchor="mm")
    draw.text((width // 2, kanji_y), kanji_text, fill=WHITE, font=f_kanji, anchor="mm")
    
    # 3. Hiragana / Furigana Reading
    if hiragana_text and hiragana_text != kanji_text:
        f_hira = get_japanese_font(44 if is_vertical else 32, bold=True)
        hira_y = kanji_y + (k_size // 2) + 38
        draw.text((width // 2, hira_y), f"【 {hiragana_text} 】", fill=ACCENT_SAKURA, font=f_hira, anchor="mm")
        romaji_y = hira_y + 54
    else:
        romaji_y = kanji_y + (k_size // 2) + 38
        
    # 4. Romaji Pronunciation
    if romaji_text:
        f_romaji = get_font(36 if is_vertical else 26, italic=True)
        draw.text((width // 2, romaji_y), romaji_text, fill=TEXT_MUTED, font=f_romaji, anchor="mm")
        eng_pill_top = romaji_y + 46
    else:
        eng_pill_top = romaji_y + 24
        
    # 5. English Translation Badge
    f_eng = get_font(48 if is_vertical else 36, bold=True)
    eng_bbox = draw.textbbox((0, 0), english_text, font=f_eng)
    eng_w = max(420, (eng_bbox[2] - eng_bbox[0]) + 90)
    eng_h = 86 if is_vertical else 64
    eng_x1 = width // 2 - eng_w // 2
    eng_y1 = eng_pill_top + 10
    
    draw.rounded_rectangle([(eng_x1, eng_y1), (eng_x1 + eng_w, eng_y1 + eng_h)], radius=20, fill=(30, 38, 56), outline=ACCENT_GOLD, width=3)
    draw.text((width // 2, eng_y1 + eng_h // 2), english_text, fill=ACCENT_GOLD, font=f_eng, anchor="mm")
    
    # 6. Example Sentence Box (PROMINENT, NO OVERFLOW)
    example_ja = item.get("example_ja", "")
    example_romaji = item.get("example_romaji", "")
    example_en = item.get("example_en", "")
    
    if example_ja:
        ex_box_y = eng_y1 + eng_h + (45 if is_vertical else 30)
        ex_box_h = card_bot - ex_box_y - 25
        
        # Deep glass container
        draw.rounded_rectangle([(card_mx + 20, ex_box_y), (width - card_mx - 20, ex_box_y + ex_box_h)], radius=22, fill=(12, 16, 26), outline=(55, 68, 92), width=2)
        
        # Example Tag Pill
        f_ex_tag = get_japanese_font(20, bold=True)
        draw.rounded_rectangle([(card_mx + 45, ex_box_y + 20), (card_mx + 225, ex_box_y + 60)], radius=14, fill=(35, 46, 68))
        draw.text((card_mx + 135, ex_box_y + 40), "例文 • EXAMPLE", fill=ACCENT_CYAN, font=f_ex_tag, anchor="mm")
        
        # Safe usable width inside example box (ensures generous 90px left/right margins)
        safe_box_w = width - (card_mx + 20) * 2 - 80
        
        f_ex_ja = get_japanese_font(52 if is_vertical else 36, bold=True)
        ja_lines = wrap_japanese_text(draw, example_ja, f_ex_ja, max_w=safe_box_w)
        
        f_ex_rom = get_font(36 if is_vertical else 26, italic=True)
        rom_lines = wrap_english_text(draw, example_romaji, f_ex_rom, max_w=safe_box_w) if example_romaji else []
        
        f_ex_en = get_font(42 if is_vertical else 30, bold=True)
        en_lines = wrap_english_text(draw, f'"{example_en}"', f_ex_en, max_w=safe_box_w) if example_en else []
        
        line_h_ja = 70 if is_vertical else 48
        line_h_rom = 50 if is_vertical else 34
        line_h_en = 56 if is_vertical else 40
        gap = 30 if is_vertical else 18
        
        curr_y = ex_box_y + (130 if is_vertical else 85)
        
        # Render Japanese Example
        for jl in ja_lines:
            draw.text((width // 2, curr_y), jl, fill=WHITE, font=f_ex_ja, anchor="mm")
            curr_y += line_h_ja
            
        # Render Romaji Example
        if rom_lines:
            curr_y += gap - (line_h_ja // 2) + (line_h_rom // 2)
            for rl in rom_lines:
                draw.text((width // 2, curr_y), rl, fill=TEXT_MUTED, font=f_ex_rom, anchor="mm")
                curr_y += line_h_rom
                
        # Render English Translation
        if en_lines:
            curr_y += gap - (line_h_rom // 2) + (line_h_en // 2)
            for el in en_lines:
                draw.text((width // 2, curr_y), el, fill=TEXT_EXAMPLE_EN, font=f_ex_en, anchor="mm")
                curr_y += line_h_en
    
    draw_footer(draw, width, height, progress=progress, is_vertical=is_vertical)
    return img

def render_outro_frame(title: str, width: int = VERTICAL_WIDTH, height: int = VERTICAL_HEIGHT, progress: float = 1.0, bg_img: Optional[Image.Image] = None) -> Image.Image:
    """Render the concluding CTA card with official website URL."""
    is_vertical = height > width
    img = create_base_canvas(width, height, bg_img)
    draw = ImageDraw.Draw(img)
    
    draw_header(img, draw, width, is_vertical=is_vertical)
    
    card_mx = 50 if is_vertical else 180
    card_top = 160 if is_vertical else 120
    card_bot = height - 140 if is_vertical else height - 100
    
    draw.rounded_rectangle([(card_mx, card_top), (width - card_mx, card_bot)], radius=24, fill=(18, 24, 38), outline=CARD_BORDER, width=2)
    
    f_cta_main = get_font(56 if is_vertical else 42, bold=True)
    f_cta_sub = get_font(30 if is_vertical else 22, bold=False)
    f_ja_bye = get_japanese_font(68 if is_vertical else 50, bold=True)
    
    center_box_y = card_top + (card_bot - card_top) // 2
    
    draw.text((width // 2, center_box_y - 280), "Great Job!", fill=ACCENT_GOLD, font=f_cta_main, anchor="mm")
    draw.text((width // 2, center_box_y - 180), "お疲れ様でした！", fill=WHITE, font=f_ja_bye, anchor="mm")
    draw.text((width // 2, center_box_y - 90), "You completed today's lesson!", fill=TEXT_MUTED, font=f_cta_sub, anchor="mm")
    
    # Follow & Website Box
    box_y = center_box_y + 10
    box_h = 270 if is_vertical else 180
    draw.rounded_rectangle([(card_mx + 30, box_y), (width - card_mx - 30, box_y + box_h)], radius=24, fill=(12, 16, 26), outline=ACCENT_RED, width=3)
    
    f_brand_big = get_font(42 if is_vertical else 32, bold=True)
    f_site_url = get_font(34 if is_vertical else 24, bold=True)
    f_sub_gold = get_font(28 if is_vertical else 20, bold=False)
    f_bye = get_japanese_font(30 if is_vertical else 22, bold=True)
    
    draw.text((width // 2, box_y + 50), "Follow Velocity Japanese", fill=WHITE, font=f_brand_big, anchor="mm")
    # Website Link Pill
    draw.rounded_rectangle([(width // 2 - 250, box_y + 88), (width // 2 + 250, box_y + 144)], radius=14, fill=ACCENT_RED)
    draw.text((width // 2, box_y + 116), WEBSITE_URL, fill=WHITE, font=f_site_url, anchor="mm")
    
    draw.text((width // 2, box_y + 175), "Free Japanese Lessons & PDFs", fill=ACCENT_GOLD, font=f_sub_gold, anchor="mm")
    draw.text((width // 2, box_y + 225), "また明日！ • See you tomorrow!", fill=TEXT_MUTED, font=f_bye, anchor="mm")
    
    draw_footer(draw, width, height, progress=progress, is_vertical=is_vertical)
    return img

def render_thumbnail(lesson: dict, width: int = VERTICAL_WIDTH, height: int = VERTICAL_HEIGHT, bg_img: Optional[Image.Image] = None) -> Image.Image:
    """Render eye-catching video thumbnail."""
    items = lesson.get("items", [])
    if items:
        return render_item_frame(items[0], 1, len(items), width, height, progress=0.0, bg_img=bg_img)
    return render_outro_frame(lesson.get("title", "Japanese Lesson"), width, height, progress=0.0, bg_img=bg_img)

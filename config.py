"""
Velocity Japanese Video Generator - Configuration (V3 Visual Masterpiece)
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output"
FONTS_DIR = BASE_DIR / "fonts"
ASSETS_DIR = BASE_DIR / "assets"
BGM_DIR = ASSETS_DIR / "bgm"
HISTORY_FILE = BASE_DIR / "history.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FONTS_DIR.mkdir(parents=True, exist_ok=True)
BGM_DIR.mkdir(parents=True, exist_ok=True)

# Official Channel Branding
CHANNEL_NAME = "Velocity Japanese"
PAGE_NAME = "Velocity Japanese"
WEBSITE_URL = "velocityjapanese.com"
TAGLINE = "Learn Japanese Daily • 日本語"
CTA_TEXT = "Visit velocityjapanese.com • Follow for Daily Lessons!"
FOOTER_TAG = "@VelocityJapanese"

# AI Configuration (Pollinations)
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY") or "sk_K98O2j1UlpALX9TBAoAuEdqxL1hpB7zh"
POLLINATIONS_ENDPOINT = "https://gen.pollinations.ai/v1/chat/completions"
AI_MODEL = os.getenv("AI_MODEL") or "openai"

# Audio Voices (edge-tts)
VOICE_JA_FEMALE = "ja-JP-NanamiNeural"  # Clear, natural female Japanese
VOICE_JA_MALE = "ja-JP-KeitaNeural"     # Deep, natural male Japanese
VOICE_EN_FEMALE = "en-US-AvaNeural"     # Clear American English female
VOICE_EN_MALE = "en-US-AndrewNeural"    # Natural American English male

DEFAULT_JA_VOICE = VOICE_JA_FEMALE
DEFAULT_EN_VOICE = VOICE_EN_MALE

# Video Dimensions (Shorts / Reels 9:16)
VERTICAL_WIDTH = 1080
VERTICAL_HEIGHT = 1920

HORIZONTAL_WIDTH = 1920
HORIZONTAL_HEIGHT = 1080

DEFAULT_FPS = 30
DEFAULT_ITEM_COUNT = 3  # 3 items for crisp ~35s Shorts/Reels!

# Premium Aesthetic Colors
DARK_BG = (10, 14, 22)           # Deep Obsidian Blue
CARD_BG = (18, 24, 38, 230)      # Frosted Semi-Transparent Glass Navy
CARD_BORDER = (55, 70, 100)      # Elegant Subtle Border
CARD_INNER_BG = (12, 16, 26, 240)# Deep Inner Box
ACCENT_RED = (255, 60, 85)       # Japanese Crimson / Torii Red
ACCENT_GOLD = (255, 204, 0)      # High-Visibility Gold Yellow
ACCENT_CYAN = (70, 180, 255)     # Electric Neon Cyan
ACCENT_SAKURA = (255, 170, 195)  # Sakura Blossom Pink
WHITE = (255, 255, 255)          # Crisp White
TEXT_MUTED = (165, 178, 200)     # Subtitle Gray
TEXT_EXAMPLE_EN = (85, 235, 160) # High-Contrast Emerald Green
DARK_LINE = (30, 38, 55)

# Curated Fallback Seed Lessons
CURATED_TOPICS = [
    {
        "category": "Days of the Week",
        "title": "Days of the Week in Japanese",
        "art_prompt": "mount fuji cherry blossoms spring kyoto temple aesthetic anime art",
        "items": [
            {
                "kanji": "月曜日",
                "hiragana": "げつようび",
                "romaji": "Getsuyōbi",
                "english": "Monday",
                "element": "月 (Moon)",
                "example_ja": "月曜日に日本語のクラスがあります。",
                "example_romaji": "Getsuyōbi ni nihongo no kurasu ga arimasu.",
                "example_en": "I have Japanese class on Monday."
            },
            {
                "kanji": "火曜日",
                "hiragana": "かようび",
                "romaji": "Kayōbi",
                "english": "Tuesday",
                "element": "火 (Fire)",
                "example_ja": "火曜日は図書館に行きます。",
                "example_romaji": "Kayōbi wa toshokan ni ikimasu.",
                "example_en": "I go to the library on Tuesday."
            },
            {
                "kanji": "水曜日",
                "hiragana": "すいようび",
                "romaji": "Suiyōbi",
                "english": "Wednesday",
                "element": "水 (Water)",
                "example_ja": "水曜日に友達と会います。",
                "example_romaji": "Suiyōbi ni tomodachi to aimasu.",
                "example_en": "I meet my friend on Wednesday."
            }
        ]
    },
    {
        "category": "Essential JLPT N5 Kanji",
        "title": "Must-Know JLPT N5 Kanji",
        "art_prompt": "traditional japanese pagoda garden stone lanterns aesthetic anime art",
        "items": [
            {
                "kanji": "日",
                "hiragana": "ひ",
                "romaji": "hi",
                "english": "Sun / Day",
                "element": "Nature & Time",
                "example_ja": "今日はとてもいい日ですね。",
                "example_romaji": "Kyō wa totemo ii hi desu ne.",
                "example_en": "Today is a very nice day, isn't it?"
            },
            {
                "kanji": "月",
                "hiragana": "つき",
                "romaji": "tsuki",
                "english": "Moon / Month",
                "element": "Nature & Time",
                "example_ja": "今夜は月がとても綺麗です。",
                "example_romaji": "Konya wa tsuki ga totemo kirei desu.",
                "example_en": "The moon is very beautiful tonight."
            },
            {
                "kanji": "水",
                "hiragana": "みず",
                "romaji": "mizu",
                "english": "Water",
                "element": "Essential",
                "example_ja": "冷たい水を一杯ください。",
                "example_romaji": "Tsumetai mizu o ippai kudasai.",
                "example_en": "Please give me a glass of cold water."
            }
        ]
    },
    {
        "category": "Useful Daily Phrases",
        "title": "Everyday Essential Japanese Phrases",
        "art_prompt": "cozy tokyo shibuya cafe street morning sun aesthetic anime art",
        "items": [
            {
                "kanji": "おはようございます",
                "hiragana": "おはようございます",
                "romaji": "Ohayō gozaimasu",
                "english": "Good morning",
                "element": "Greeting",
                "example_ja": "皆さん、おはようございます！",
                "example_romaji": "Minasan, ohayō gozaimasu!",
                "example_en": "Good morning, everyone!"
            },
            {
                "kanji": "ありがとうございます",
                "hiragana": "ありがとうございます",
                "romaji": "Arigatō gozaimasu",
                "english": "Thank you very much",
                "element": "Polite",
                "example_ja": "手伝ってくれてありがとうございます。",
                "example_romaji": "Tetsudatte kurete arigatō gozaimasu.",
                "example_en": "Thank you very much for helping me."
            },
            {
                "kanji": "すみません",
                "hiragana": "すみません",
                "romaji": "Sumimasen",
                "english": "Excuse me / Sorry",
                "element": "Crucial",
                "example_ja": "すみません、駅はどこですか？",
                "example_romaji": "Sumimasen, eki wa doko desu ka?",
                "example_en": "Excuse me, where is the train station?"
            }
        ]
    }
]

# Categorized Massive Topic Bank for Forever-Run Automation
CATEGORIZED_TOPICS = {
    "JLPT N5 & Kanji": [
        ("Must-Know JLPT N5 Action Verbs", "traditional japanese house tatami room morning anime art"),
        ("Core JLPT N5 Kanji: Nature & Elements", "kyoto bamboo forest green serene aesthetic anime art"),
        ("Core JLPT N5 Kanji: People & Relationships", "japanese family park picnic cherry blossoms anime art"),
        ("Core JLPT N5 Kanji: Time & Calendar", "japanese antique clock traditional room warm light anime art"),
        ("Core JLPT N5 Kanji: Directions & Locations", "tokyo street crossing signposts sunset anime art")
    ],
    "Food & Dining": [
        ("Ordering at a Japanese Ramen Restaurant", "cozy japanese ramen bar shop counter steam delicious anime art"),
        ("Essential Japanese Izakaya Phrases", "tokyo izakaya lanterns glowing cozy night atmosphere anime art"),
        ("Must-Know Japanese Street Food", "osaka dotonbori street food stalls festival lights anime art"),
        ("Words for Flavors & Tastes in Japan", "japanese matcha tea sweets traditional cafe aesthetic anime art"),
        ("Convenience Store (Konbini) Japanese", "japanese 7-eleven lawson illuminated night street anime art"),
        ("Ordering Coffee at a Tokyo Cafe", "modern tokyo omotesando cafe wooden interior warm latte anime art")
    ],
    "Tokyo Travel & Transit": [
        ("Tokyo Train & Subway Essential Phrases", "tokyo shinjuku train platform sunset sky aesthetic anime art"),
        ("Asking for Directions in Tokyo", "tokyo shibuya crossing rainy night neon reflections anime art"),
        ("Airport & Hotel Check-in Phrases", "haneda airport modern terminal glass window airplane sunrise anime art"),
        ("Shopping in Akihabara & Tokyo", "akihabara electric town anime shops colorful lights anime art"),
        ("Taking a Taxi and Bus in Japan", "tokyo city night taxi street lights bokeh aesthetic anime art"),
        ("Buying Tickets & Asking for Prices", "japanese train ticket vending machine clean aesthetic anime art")
    ],
    "Everyday Life & Routines": [
        ("Morning Routine Verbs in Japanese", "bright japanese bedroom morning sunlight balcony plants anime art"),
        ("Evening & Night Routine Japanese", "cozy japanese living room evening warm lamp tea anime art"),
        ("Japanese Weather & Four Seasons", "mount fuji snowy mountain winter wonderland anime aesthetic art"),
        ("Health & Body Parts in Japanese", "peaceful japanese zen garden cherry tree aesthetic anime art"),
        ("Describing Clothes and Fashion", "tokyo harajuku stylish fashion boutique street anime art")
    ],
    "Conversations & Expressions": [
        ("Common Japanese Reaction Words", "japanese friends talking laughing rooftop sunset anime art"),
        ("Expressions of Gratitude & Apology", "traditional japanese bow greeting polite tatami room anime art"),
        ("How to Express Likes and Dislikes", "japanese anime cute room hobbies books music anime art"),
        ("Japanese Question Words (5Ws & 1H)", "tokyo library bookshelf warm lighting study aesthetic anime art"),
        ("Natural Fillers & Conversation Starters", "tokyo evening riverside walking path lanterns anime art")
    ],
    "Culture & Anime": [
        ("Japanese Festival (Matsuri) Words", "japanese summer festival fireworks yukata lanterns anime art"),
        ("Cherry Blossom (Sakura) Season Words", "cherry blossom petals falling river meguro tokyo anime art"),
        ("Anime Slang Every Fan Should Know", "japanese manga workshop desk drawing anime art"),
        ("Cute Japanese Animal Vocabulary", "nara deer park temple morning sun peaceful anime art")
    ]
}

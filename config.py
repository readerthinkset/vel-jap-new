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
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
POLLINATIONS_ENDPOINT = "https://gen.pollinations.ai/v1/chat/completions"
AI_MODEL = os.getenv("AI_MODEL") or "openai"
IMAGE_MODEL = os.getenv("IMAGE_MODEL") or "flux"

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

# Categorized Massive Topic Bank for Forever-Run Automation (100+ Curated Topics)
CATEGORIZED_TOPICS = {
    "JLPT N5 & Core Kanji": [
        ("Must-Know JLPT N5 Action Verbs", "traditional japanese house tatami room morning anime art"),
        ("Core JLPT N5 Kanji: Nature & Elements", "kyoto bamboo forest green serene aesthetic anime art"),
        ("Core JLPT N5 Kanji: People & Relationships", "japanese family park picnic cherry blossoms anime art"),
        ("Core JLPT N5 Kanji: Time & Calendar", "japanese antique clock traditional room warm light anime art"),
        ("Core JLPT N5 Kanji: Directions & Locations", "tokyo street crossing signposts sunset anime art"),
        ("Core JLPT N5 Adjectives for Everyday Objects", "japanese traditional living room tea set sunny day anime art"),
        ("Must-Know Japanese Opposites (Big/Small, Hot/Cold)", "kyoto traditional wooden street warm and cool tones anime art"),
        ("Essential Japanese Movement Verbs (Go, Come, Return)", "tokyo commuter railway station sunny morning anime art"),
        ("Expressing Ability with Potential Verbs in Japanese", "japanese high school rooftop blue sky clouds anime art"),
        ("Japanese Numbers, Counters and Quantities", "japanese market stall cute goods organized aesthetic anime art"),
        ("Basic Japanese Colors in Daily Life", "traditional japanese painting pigments colorful palette anime art"),
        ("Days, Months, and Counting Time in Japanese", "tokyo desk calendar sakura blossom window view anime art"),
        ("Essential Japanese Question Particles and Words", "tokyo university library wooden tables warm lamps anime art")
    ],
    "Food & Dining Across Japan": [
        ("Ordering at a Japanese Ramen Restaurant", "cozy japanese ramen bar shop counter steam delicious anime art"),
        ("Essential Japanese Izakaya Phrases", "tokyo izakaya lanterns glowing cozy night atmosphere anime art"),
        ("Must-Know Japanese Street Food", "osaka dotonbori street food stalls festival lights anime art"),
        ("Words for Flavors & Tastes in Japan", "japanese matcha tea sweets traditional cafe aesthetic anime art"),
        ("Convenience Store (Konbini) Japanese", "japanese 7-eleven lawson illuminated night street anime art"),
        ("Ordering Coffee at a Tokyo Cafe", "modern tokyo omotesando cafe wooden interior warm latte anime art"),
        ("Sushi Restaurant Dining Etiquette & Ordering", "elegant ginza sushi bar wooden counter master chef anime art"),
        ("Japanese Bakery Delights (Melonpan & Shokupan)", "cozy tokyo bakery morning golden fresh bread display anime art"),
        ("Japanese Supermarket Shopping & Food Labels", "organized tokyo supermarket fresh bento grocery anime art"),
        ("Dining at a Japanese Curry House", "steaming japanese katsu curry booth warm diner anime art"),
        ("Traditional Japanese Tea Ceremony Vocabulary", "zen tea room tatami tatami garden green matcha bowl anime art"),
        ("Japanese Yakitori & Skewer Bar Phrases", "smoky tokyo yakitori alley red paper lanterns anime art"),
        ("Japanese Table Manners & Meal Etiquette Phrases", "traditional japanese dining table lacquer bowls steam anime art")
    ],
    "Tokyo & Regional Travel & Transit": [
        ("Tokyo Train & Subway Essential Phrases", "tokyo shinjuku train platform sunset sky aesthetic anime art"),
        ("Asking for Directions in Tokyo", "tokyo shibuya crossing rainy night neon reflections anime art"),
        ("Airport & Hotel Check-in Phrases", "haneda airport modern terminal glass window airplane sunrise anime art"),
        ("Shopping in Akihabara & Tokyo", "akihabara electric town anime shops colorful lights anime art"),
        ("Taking a Taxi and Bus in Japan", "tokyo city night taxi street lights bokeh aesthetic anime art"),
        ("Buying Tickets & Asking for Prices", "japanese train ticket vending machine clean aesthetic anime art"),
        ("Riding the Shinkansen Bullet Train", "shinkansen bullet train passing mount fuji clear morning anime art"),
        ("Staying at a Traditional Japanese Ryokan Inn", "hot spring ryokan wooden bath sliding shoji screens anime art"),
        ("Navigating Japan's IC Cards (Suica & Pasmo)", "tokyo subway turnstile ticket gate commuters anime art"),
        ("Visiting Ancient Temples and Shrines in Kyoto", "red fushimi inari torii gates path morning mist anime art"),
        ("Sightseeing in Historic Asakusa and Sensoji", "asakusa sensoji temple thunder gate giant lantern anime art"),
        ("Handling Lost Property (Wasuremono) in Japan", "tokyo station lost and found clean customer desk anime art"),
        ("Emergency and Helpful Travel Phrases", "tokyo neighborhood police koban warm light night anime art")
    ],
    "Everyday Life & Routines": [
        ("Morning Routine Verbs in Japanese", "bright japanese bedroom morning sunlight balcony plants anime art"),
        ("Evening & Night Routine Japanese", "cozy japanese living room evening warm lamp tea anime art"),
        ("Japanese Weather & Four Seasons", "mount fuji snowy mountain winter wonderland anime aesthetic art"),
        ("Health & Body Parts in Japanese", "peaceful japanese zen garden cherry tree aesthetic anime art"),
        ("Describing Clothes and Fashion", "tokyo harajuku stylish fashion boutique street anime art"),
        ("Household Chores and Cleaning in Japanese", "bright japanese kitchen tidy organized sunshine anime art"),
        ("Visiting a Japanese Pharmacy & Medicine", "bright tokyo drugstore cosmetic pharmacy shelves anime art"),
        ("Japanese Post Office & Mailing Letters", "japanese red mailbox post office neighborhood street anime art"),
        ("Cooking and Kitchen Utensils in Japanese", "japanese home kitchen wooden cutting board miso soup anime art"),
        ("Daily Fitness & Sports Vocabulary", "japanese riverside running trail joggers sunset anime art"),
        ("Sleeping and Waking Up Expressions", "japanese futon tatami room gentle moonlight calm anime art"),
        ("Home & Apartment Living Vocabulary", "cozy japanese apartment balcony overlooking city sunset anime art")
    ],
    "Conversations, Reactions & Natural Nuances": [
        ("Common Japanese Reaction Words", "japanese friends talking laughing rooftop sunset anime art"),
        ("Expressions of Gratitude & Apology", "traditional japanese bow greeting polite tatami room anime art"),
        ("How to Express Likes and Dislikes", "japanese anime cute room hobbies books music anime art"),
        ("Japanese Question Words (5Ws & 1H)", "tokyo library bookshelf warm lighting study aesthetic anime art"),
        ("Natural Fillers & Conversation Starters", "tokyo evening riverside walking path lanterns anime art"),
        ("Giving and Receiving Compliments in Japanese", "cheerful japanese friends cafe chat smiling warm anime art"),
        ("Agreeing and Disagreeing Politely in Japanese", "japanese cozy meeting room window soft daylight anime art"),
        ("Expressing Surprise and Amazement", "tokyo fireworks festival amazed friends looking up anime art"),
        ("Saying Goodbye and Goodnight in Different Ways", "tokyo train station farewell wave dusk twilight anime art"),
        ("How to Ask for Help or Favors in Japanese", "friendly japanese neighborhood walkway daytime anime art"),
        ("Casual Japanese Slang for Close Friends", "tokyo youth hangout arcade game neon colorful anime art")
    ],
    "Anime, Manga & Japanese Pop Culture": [
        ("Anime Slang Every Fan Should Know", "japanese manga workshop desk drawing anime art"),
        ("Cute Japanese Animal Vocabulary", "nara deer park temple morning sun peaceful anime art"),
        ("Gacha, Arcades & Claw Machine Phrases", "tokyo akihabara claw machine arcade colorful neon anime art"),
        ("Manga and Comic Sound Effects (Onomatopoeia)", "artistic manga studio ink bottles manuscript paper anime art"),
        ("Idol & J-Pop Concert Culture Phrases", "japanese concert arena glow sticks colorful light ocean anime art"),
        ("Cosplay & Convention Terminology in Japan", "tokyo big sight convention hall lively crowd anime art"),
        ("Karaoke Singing and Booking in Tokyo", "cozy private karaoke room neon disco mic screen anime art"),
        ("Video Game and RPG Vocabulary in Japanese", "gamer setup cozy dark room glowing keyboard screens anime art"),
        ("Japanese Mascot (Yuru-chara) Culture Words", "cute japanese mascot character festival stage sunny anime art")
    ],
    "Four Seasons, Nature & Festivals": [
        ("Japanese Festival (Matsuri) Words", "japanese summer festival fireworks yukata lanterns anime art"),
        ("Cherry Blossom (Sakura) Season Words", "cherry blossom petals falling river meguro tokyo anime art"),
        ("Autumn Foliage (Momijigari) Japanese", "kyoto golden maple leaves red autumn temple garden anime art"),
        ("Winter Snow and Hot Springs (Onsen) in Japan", "hokkaido snowy outdoor onsen steam pine trees anime art"),
        ("Summer Tanabata Star Festival Phrases", "bamboo branches colorful paper wishes starry night anime art"),
        ("New Year Celebrations (Oshogatsu) in Japan", "traditional japanese new year shrine visit sunrise anime art"),
        ("Japanese Rain & Umbrella Season (Tsuyu)", "tokyo rainy street colorful umbrellas reflections anime art"),
        ("Summer Vacation (Natsuyasumi) Countryside Words", "countryside japanese railway crossing summer clouds sky anime art"),
        ("Moon Viewing Festival (Tsukimi) Words", "full moon night pampas grass dango skewers veranda anime art")
    ],
    "Emotions, Feelings & Social Courtesy": [
        ("Expressing Joy and Happiness in Japanese", "japanese sunny park green grass laughing smiling anime art"),
        ("Expressing Tiredness, Relief and Relaxation", "peaceful japanese engawa porch breezy afternoon tea anime art"),
        ("Words for Encouragement (Ganbatte & More)", "japanese sports club track sunrise energetic anime art"),
        ("Handling Difficult Situations with Calm (Shouganai)", "quiet tokyo street evening calm peaceful breeze anime art"),
        ("Polite Japanese Business Greetings (Keigo Basics)", "modern tokyo office skyscraper glass windows suit anime art"),
        ("Giving Gifts and Souvenirs (Omiyage) in Japan", "beautiful japanese gift box wrapping cloth furoshiki anime art"),
        ("Expressing Hunger and Thirst Naturally", "tokyo bustling food market aroma steam appetizing anime art")
    ]
}


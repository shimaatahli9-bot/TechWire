import feedparser
import json
import re
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncio
import logging
import google.generativeai as genai

from database import generate_id, insert_news, get_setting, set_setting, get_sources
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('murrasil.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CATEGORIES = ["نماذج AI", "أبحاث", "أدوات", "شركات ناشئة", "أجهزة", "سياسات"]

_last_error_shown = False


def clean_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def detect_category(title: str, content: str) -> str:
    text = (title + " " + content).lower()
    
    if any(kw in text for kw in ["model", "gpt", "llm", "llama", "claude", "gemini", "transformer", "diffusion"]):
        return "نماذج AI"
    if any(kw in text for kw in ["research", "paper", "arxiv", "study", "algorithm", "training"]):
        return "أبحاث"
    if any(kw in text for kw in ["tool", "platform", "api", "sdk", "library", "framework", "open source"]):
        return "أدوات"
    if any(kw in text for kw in ["startup", "funding", "investment", "raise", "acqui", "million", "billion"]):
        return "شركات ناشئة"
    if any(kw in text for kw in ["hardware", "chip", "gpu", "nvidia", "processor", "device", "phone", "laptop"]):
        return "أجهزة"
    if any(kw in text for kw in ["policy", "regulation", "law", "government", "ban", "restrict", "ethics"]):
        return "سياسات"
    
    return "نماذج AI"


def call_ai(prompt: str) -> Optional[str]:
    global _last_error_shown
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set")
        return None
    
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Gemini API error: {error_msg}")
        if "quota" in error_msg.lower() or "auth" in error_msg.lower() or "api_key" in error_msg.lower():
            if not _last_error_shown:
                _last_error_shown = True
                print("\n⚠️ خطأ في الاتصال بـ Gemini API — تحقق من المفتاح في ملف .env\n")
        return None


async def call_ai_async(prompt: str) -> Optional[str]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, call_ai, prompt)


async def summarize_article(title: str, content: str) -> Optional[Dict[str, str]]:
    prompt = f"""You are a tech journalist. Given this news article title and content in English,
return a JSON object with:
- "title_ar": Arabic translation of the title (concise, journalistic)
- "summary_ar": 2-3 sentence Arabic summary of the article
- "category": one of [نماذج AI, أبحاث, أدوات, شركات ناشئة, أجهزة, سياسات]

Article title: {title}
Article content/description: {content[:2000]}

Return ONLY valid JSON, no explanation."""

    response = await call_ai_async(prompt)
    if not response:
        return None
    
    try:
        json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return {
                "title_ar": result.get("title_ar", title),
                "summary_ar": result.get("summary_ar", ""),
                "category": result.get("category", detect_category(title, content))
            }
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
    
    return {
        "title_ar": title,
        "summary_ar": content[:300] if content else "",
        "category": detect_category(title, content)
    }


async def fetch_feed(source: Dict) -> List[Dict[str, Any]]:
    news_items = []
    try:
        feed = feedparser.parse(source["url"])
        if feed.bozo and feed.bozo_exception:
            logger.warning(f"Feed parse warning for {source['name']}: {feed.bozo_exception}")
        
        for entry in feed.entries[:20]:
            news_id = generate_id(entry.link)
            title = entry.get("title", "No title")
            content = entry.get("summary") or entry.get("description") or entry.get("content", "")
            if isinstance(content, list):
                content = " ".join([c.get("value", "") for c in content])
            content = clean_html(content)
            
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            published_at = datetime(*published[:6]).isoformat() if published else datetime.now().isoformat()
            
            news_items.append({
                "id": news_id,
                "title": title,
                "content": content,
                "original_url": entry.link,
                "published_at": published_at,
                "source_name": source["name"],
                "source_url": source["url"]
            })
    except Exception as e:
        logger.error(f"Error fetching {source['name']}: {e}")
    
    return news_items


async def fetch_all_news() -> int:
    sources = get_sources()
    enabled_sources = [s for s in sources if s["enabled"]]
    
    last_fetch = get_setting("last_fetch_time")
    last_fetch_time = datetime.fromisoformat(last_fetch) if last_fetch else None
    
    new_count = 0
    
    for source in enabled_sources:
        items = await fetch_feed(source)
        for item in items:
            if last_fetch_time:
                try:
                    item_time = datetime.fromisoformat(item["published_at"])
                    if item_time < last_fetch_time:
                        continue
                except:
                    pass
            
            result = await summarize_article(item["title"], item["content"])
            if result:
                news_data = {
                    "id": item["id"],
                    "title_ar": result["title_ar"],
                    "summary_ar": result["summary_ar"],
                    "source_name": item["source_name"],
                    "source_url": item["source_url"],
                    "original_url": item["original_url"],
                    "published_at": item["published_at"],
                    "category": result["category"]
                }
                if insert_news(news_data):
                    new_count += 1
                    logger.info(f"Added: {result['title_ar'][:50]}...")
            
            await asyncio.sleep(0.5)
    
    set_setting("last_fetch_time", datetime.now().isoformat())
    logger.info(f"Fetch complete. {new_count} new articles.")
    return new_count


def test_gemini_connection() -> bool:
    try:
        response = gemini_model.generate_content("Say 'OK' if you can read this.")
        if response.text:
            logger.info("Gemini API connection successful")
            return True
    except Exception as e:
        logger.error(f"Gemini API connection failed: {e}")
        return False
    return False

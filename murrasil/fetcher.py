import feedparser
import json
import re
from datetime import datetime
from typing import Optional, Dict, Any, List
import aiohttp
import asyncio
import logging

from database import generate_id, insert_news, get_setting, set_setting, get_sources
from config import OPENAI_API_KEY, AI_MODEL, OLLAMA_BASE_URL

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


async def call_ai_openai(prompt: str) -> Optional[str]:
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set")
        return None
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": AI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    logger.error(f"OpenAI API error: {response.status} - {error_text}")
                    return None
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return None


async def call_ai_ollama(prompt: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            data = {
                "model": AI_MODEL.replace("ollama:", ""),
                "prompt": prompt,
                "stream": False
            }
            async with session.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "")
                else:
                    error_text = await response.text()
                    logger.error(f"Ollama API error: {response.status} - {error_text}")
                    return None
    except Exception as e:
        logger.error(f"Ollama API call failed: {e}")
        return None


async def call_ai(prompt: str) -> Optional[str]:
    if AI_MODEL.startswith("ollama:"):
        return await call_ai_ollama(prompt)
    return await call_ai_openai(prompt)


async def summarize_article(title: str, content: str) -> Optional[Dict[str, str]]:
    prompt = f"""You are a tech journalist. Given this news article title and content in English,
return a JSON object with:
- "title_ar": Arabic translation of the title (concise, journalistic)
- "summary_ar": 2-3 sentence Arabic summary of the article
- "category": one of [نماذج AI, أبحاث, أدوات, شركات ناشئة, أجهزة, سياسات]

Article title: {title}
Article content/description: {content[:2000]}

Return ONLY valid JSON, no explanation."""

    response = await call_ai(prompt)
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

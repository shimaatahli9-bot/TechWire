import re
import logging
from typing import Optional
import aiohttp

from config import OPENAI_API_KEY, AI_MODEL, OLLAMA_BASE_URL
from database import get_news_by_id, update_news_article

logger = logging.getLogger(__name__)


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
                "temperature": 0.8,
                "max_tokens": 1500
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


async def generate_article(news_id: str) -> Optional[str]:
    news = get_news_by_id(news_id)
    if not news:
        logger.error(f"News not found: {news_id}")
        return None
    
    prompt = f"""أنت صحفي تقني محترف. اكتب مقالاً إخبارياً قصيراً باللغة العربية الفصحى عن الخبر التالي.

المقال يجب أن يكون:
- بين 150 و 250 كلمة
- يبدأ بعنوان جذاب (مختلف عن العنوان الأصلي)
- يتضمن: مقدمة، تفاصيل أساسية (من؟ ماذا؟ لماذا يهم؟)، خاتمة تحليلية قصيرة
- بأسلوب إخباري احترافي

عنوان الخبر: {news['title_ar']}
ملخص الخبر: {news['summary_ar']}
المصدر: {news['source_name']}"""

    article = await call_ai(prompt)
    if article:
        update_news_article(news_id, article)
        logger.info(f"Article generated for: {news_id}")
        return article
    
    return None

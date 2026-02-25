import re
import logging
import asyncio
from typing import Optional
import google.generativeai as genai

from config import GEMINI_API_KEY
from database import get_news_by_id, update_news_article

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

logger = logging.getLogger(__name__)


def call_ai(prompt: str) -> Optional[str]:
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set")
        return None
    
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None


async def call_ai_async(prompt: str) -> Optional[str]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, call_ai, prompt)


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

    article = await call_ai_async(prompt)
    if article:
        update_news_article(news_id, article)
        logger.info(f"Article generated for: {news_id}")
        return article
    
    return None

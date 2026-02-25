import sqlite3
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import json

DATABASE_PATH = "news.db"

DEFAULT_SOURCES = [
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("Wired AI", "https://www.wired.com/feed/tag/ai/latest/rss"),
    ("THE DECODER", "https://the-decoder.com/feed/"),
    ("Hugging Face Blog", "https://huggingface.co/blog/feed.xml"),
    ("OpenAI Blog", "https://openai.com/blog/rss.xml"),
    ("Google AI Blog", "http://googleaiblog.blogspot.com/atom.xml"),
    ("Hacker News", "https://news.ycombinator.com/rss"),
    ("Reddit ML", "https://www.reddit.com/r/MachineLearning/.rss"),
    ("arXiv cs.AI", "https://arxiv.org/rss/cs.AI"),
    ("arXiv cs.LG", "https://arxiv.org/rss/cs.LG"),
    ("DeepMind Blog", "https://deepmind.com/blog/feed/basic/"),
    ("The Rundown AI", "https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml"),
    ("Unite.AI", "https://www.unite.ai/feed/"),
    ("MarkTechPost", "https://www.marktechpost.com/feed"),
    ("SiliconANGLE AI", "https://siliconangle.com/category/ai/feed"),
    ("LangChain Blog", "https://blog.langchain.dev/rss/"),
    ("NVIDIA Blog", "https://developer.nvidia.com/blog/feed"),
    ("r/artificial", "https://www.reddit.com/r/artificial/.rss"),
    ("cs.CL NLP", "https://arxiv.org/rss/cs.CL"),
    ("cs.CV", "https://arxiv.org/rss/cs.CV"),
    ("Product Hunt", "https://www.producthunt.com/feed"),
    ("Digital Trends", "https://www.digitaltrends.com/feed/"),
    ("Engadget", "https://www.engadget.com/rss.xml"),
    ("IEEE Spectrum", "https://feeds.feedburner.com/IeeeSpectrum"),
    ("TechRadar", "https://www.techradar.com/feeds.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("Bloomberg Tech", "https://feeds.bloomberg.com/technology/news.rss"),
    ("Apple Insider", "https://appleinsider.com/rss/news/"),
    ("GeekWire", "https://www.geekwire.com/feed/"),
    ("Microsoft Blog", "https://blogs.microsoft.com/feed/"),
    ("Google Blog", "https://blog.google/rss/"),
]


@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id TEXT PRIMARY KEY,
                title_ar TEXT,
                summary_ar TEXT,
                article_ar TEXT,
                source_name TEXT,
                source_url TEXT,
                original_url TEXT,
                published_at TEXT,
                fetched_at TEXT,
                category TEXT,
                status TEXT DEFAULT 'new'
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                enabled INTEGER DEFAULT 1
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM sources")
        if cursor.fetchone()[0] == 0:
            for name, url in DEFAULT_SOURCES:
                cursor.execute(
                    "INSERT INTO sources (name, url, enabled) VALUES (?, ?, 1)",
                    (name, url)
                )
        default_settings = {
            "fetch_interval_minutes": "15",
            "max_news_age_hours": "48",
            "last_fetch_time": "",
        }
        for key, value in default_settings.items():
            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                (key, value)
            )
        conn.commit()


def generate_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def insert_news(news_item: Dict[str, Any]) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO news (id, title_ar, summary_ar, article_ar, source_name,
                                  source_url, original_url, published_at, fetched_at,
                                  category, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                news_item["id"],
                news_item.get("title_ar", ""),
                news_item.get("summary_ar", ""),
                news_item.get("article_ar"),
                news_item.get("source_name", ""),
                news_item.get("source_url", ""),
                news_item.get("original_url", ""),
                news_item.get("published_at", ""),
                news_item.get("fetched_at", datetime.now().isoformat()),
                news_item.get("category", ""),
                "new"
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def get_news(status: str = "new", page: int = 1, limit: int = 20) -> List[Dict]:
    offset = (page - 1) * limit
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM news 
            WHERE status = ? 
            ORDER BY fetched_at DESC 
            LIMIT ? OFFSET ?
        """, (status, limit, offset))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_news_counts() -> Dict[str, int]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as count FROM news GROUP BY status")
        rows = cursor.fetchall()
        counts = {"new": 0, "approved": 0, "rejected": 0}
        for row in rows:
            if row["status"] in counts:
                counts[row["status"]] = row["count"]
        return counts


def update_news_status(news_id: str, status: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE news SET status = ? WHERE id = ?",
            (status, news_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def update_news_article(news_id: str, article: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE news SET article_ar = ?, status = 'approved' WHERE id = ?",
            (article, news_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def get_news_by_id(news_id: str) -> Optional[Dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (news_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_sources() -> List[Dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources ORDER BY id")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def add_source(name: str, url: str) -> Dict:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sources (name, url, enabled) VALUES (?, ?, 1)",
            (name, url)
        )
        conn.commit()
        return {"id": cursor.lastrowid, "name": name, "url": url, "enabled": 1}


def update_source(source_id: int, enabled: bool) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sources SET enabled = ? WHERE id = ?",
            (1 if enabled else 0, source_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_source(source_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sources WHERE id = ?", (source_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_setting(key: str) -> Optional[str]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else None


def set_setting(key: str, value: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
        conn.commit()


def get_all_settings() -> Dict[str, str]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        rows = cursor.fetchall()
        return {row["key"]: row["value"] for row in rows}


def cleanup_old_news(max_age_hours: int = 48):
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM news WHERE fetched_at < ? AND status = 'rejected'",
            (cutoff.isoformat(),)
        )
        conn.commit()

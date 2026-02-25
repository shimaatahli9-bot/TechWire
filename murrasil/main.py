from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import os

from database import (
    init_db, get_news, get_news_counts, update_news_status,
    get_sources, add_source, update_source, delete_source,
    get_all_settings, set_setting, cleanup_old_news
)
from fetcher import fetch_all_news, test_gemini_connection
from ai_writer import generate_article
from config import HOST, PORT, FETCH_INTERVAL_MINUTES, MAX_NEWS_AGE_HOURS
from scheduler import start_scheduler

app = FastAPI(title="مُراسِل", description="AI-powered Arabic tech news curation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


class SourceCreate(BaseModel):
    name: str
    url: str


class SettingsUpdate(BaseModel):
    settings: dict


@app.on_event("startup")
async def startup_event():
    init_db()
    test_gemini_connection()
    start_scheduler()
    asyncio.create_task(run_cleanup_periodically())


async def run_cleanup_periodically():
    while True:
        await asyncio.sleep(3600)
        cleanup_old_news(MAX_NEWS_AGE_HOURS)


@app.get("/")
async def root():
    return FileResponse(os.path.join(static_path, "index.html"))


@app.get("/api/news")
async def api_get_news(status: str = "new", page: int = 1, limit: int = 20):
    news = get_news(status, page, limit)
    return {"news": news, "page": page, "status": status}


@app.get("/api/news/counts")
async def api_get_counts():
    return get_news_counts()


@app.post("/api/news/{news_id}/approve")
async def api_approve_news(news_id: str):
    article = await generate_article(news_id)
    if article:
        return {"success": True, "article": article}
    raise HTTPException(status_code=500, detail="Failed to generate article")


@app.post("/api/news/{news_id}/reject")
async def api_reject_news(news_id: str):
    if update_news_status(news_id, "rejected"):
        return {"success": True}
    raise HTTPException(status_code=404, detail="News not found")


@app.post("/api/news/{news_id}/restore")
async def api_restore_news(news_id: str):
    if update_news_status(news_id, "new"):
        return {"success": True}
    raise HTTPException(status_code=404, detail="News not found")


@app.post("/api/news/fetch")
async def api_fetch_news(background_tasks: BackgroundTasks):
    new_count = await fetch_all_news()
    return {"success": True, "new_count": new_count}


@app.get("/api/sources")
async def api_get_sources():
    return {"sources": get_sources()}


@app.post("/api/sources")
async def api_add_source(source: SourceCreate):
    result = add_source(source.name, source.url)
    return {"success": True, "source": result}


@app.put("/api/sources/{source_id}")
async def api_toggle_source(source_id: int, enabled: bool = True):
    if update_source(source_id, enabled):
        return {"success": True}
    raise HTTPException(status_code=404, detail="Source not found")


@app.delete("/api/sources/{source_id}")
async def api_delete_source(source_id: int):
    if delete_source(source_id):
        return {"success": True}
    raise HTTPException(status_code=404, detail="Source not found")


@app.get("/api/settings")
async def api_get_settings():
    return get_all_settings()


@app.post("/api/settings")
async def api_update_settings(settings: SettingsUpdate):
    for key, value in settings.settings.items():
        set_setting(key, str(value))
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=False
    )

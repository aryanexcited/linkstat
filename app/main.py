from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime, timedelta, timezone
from app.database import get_db
from app import models, schemas
from app.utils import encode_base62

app = FastAPI(title="linkstat")

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}

@app.post("/shorten", response_model=schemas.URLResponse, status_code=201)
def shorten_url(payload: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    if payload.custom_slug:
        existing = db.query(models.URL).filter(
            models.URL.short_code == payload.custom_slug
        ).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Custom slug '{payload.custom_slug} is already in use'"
            )
        new_url = models.URL(
            short_code = payload.custom_slug,
            original_url = str(payload.original_url)
        )
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
    else:
        new_url = models.URL(short_code="", original_url=str(payload.original_url))
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        new_url.short_code = encode_base62(new_url.id)
        db.commit()
        db.refresh(new_url)
    base_url = str(request.base_url).rstrip("/")
    return schemas.URLResponse(
        short_code=new_url.short_code,
        original_url=new_url.original_url,
        short_url=f"{base_url}/{new_url.short_code}",
        created_at=new_url.created_at
    )

@app.get("/stats/{short_code}", response_model=schemas.StatsResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if not url_entry:
        return HTTPException(status_code=404, detail="Short URL not found")
    
    total_clicks = db.query(func.count(models.Click.id)).filter(
        models.Click.url_id == url_entry.id
    ).scalar()

    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=6)

    daily_counts = db.query(
        func.date(models.Click.clicked_at).label("day"),
        func.count(models.Click.id).label("count")
    ).filter(
        models.Click.url_id == url_entry.id,
        models.Click.clicked_at >= seven_days_ago
    ).group_by(func.date(models.Click.clicked_at)).all()

    count_by_date = {str(row.day): row.count for row in daily_counts}

    clicks_last_7_days = []
    for i in range(6, -1, -1):
        day = (datetime.now(timezone.utc) - timedelta(days=i)).date()
        days_str = str(day)
        clicks_last_7_days.append(
                schemas.ClicksByDay(date=days_str, clicks=count_by_date.get(days_str, 0))
        )
    
    return schemas.StatsResponse(
        short_code = url_entry.short_code,
        original_url = url_entry.original_url,
        total_clicks=total_clicks,
        clicks_last_7_days = clicks_last_7_days
    )

@app.get("/{short_code}")
def redirect_to_original(short_code: str, request: Request, db: Session = Depends(get_db)):
    url_entry = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    new_click = models.Click(
        url_id=url_entry.id,
        referrer=request.headers.get("referrer")
    )
    db.add(new_click)
    db.commit()

    return RedirectResponse(url=url_entry.original_url, status_code=302)

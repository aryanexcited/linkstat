from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
import re
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_slug: Optional[str] = None
    @field_validator("custom_slug")
    @classmethod
    def validate_slug(cls, v):
        if v is None:
            return v
        if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", v):
            raise ValueError(
                "Custom slug must contain only alphanumerics, hyphens, and underscores"
            )
        reserved = {"health", "shorten", "stats", "docs", "openapi.json", "redoc"}
        if v.lower() in reserved:
            raise ValueError(
                f"'{v}' is a reserved word and cannot be use as a custiom slug"
            )
        return v

class URLResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class ClicksByDay(BaseModel):
    date: str
    clicks: int

class StatsResponse(BaseModel):
    short_code: str
    original_url: str
    total_clicks: int
    clicks_last_7_days: list[ClicksByDay]


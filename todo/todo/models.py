"""Pydantic models for todo API."""

from datetime import datetime
from typing import Optional

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = object


class TodoBase(BaseModel):
    """Base todo model."""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoCreate(TodoBase):
    """Todo creation model."""
    pass


class TodoUpdate(BaseModel):
    """Todo update model."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    """Todo response model."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    if hasattr(BaseModel, 'Config'):
        class Config:
            from_attributes = True
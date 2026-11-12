"""
StoryWeave AI - Chapter Schemas

Request and response validation models for Chapter management.
Preserves original manuscript content and tracks processing status.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, model_validator
from app.schemas.common import PaginatedResponse


class ProcessingStatus(str, Enum):
    """Processing lifecycle status for chapter ingestion & AI analysis."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ChapterBase(BaseModel):
    """Base chapter properties."""

    title: str = Field(..., min_length=1, max_length=200, description="Chapter title")
    chapter_number: int = Field(..., ge=1, description="Chapter sequence number (1, 2, 3...)")
    content: str = Field(..., min_length=1, description="Chapter text content / manuscript")


class ChapterCreate(ChapterBase):
    """Payload for submitting a new chapter."""
    pass


class ChapterUpdate(BaseModel):
    """Payload for updating chapter content or title.

    Note: Updating 'content' creates a modified working draft.
    The 'original_content' manuscript is permanently preserved.
    """

    title: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Updated chapter title")
    chapter_number: Optional[int] = Field(default=None, ge=1, description="Updated chapter number")
    content: Optional[str] = Field(default=None, min_length=1, description="Updated working manuscript content")


class ChapterResponse(BaseModel):
    """Complete chapter data returned by API.

    Guarantees preservation of the initial manuscript in 'original_content'.
    """

    id: str = Field(..., description="Unique chapter ID")
    story_id: str = Field(..., description="Parent story ID")
    user_id: str = Field(..., description="Owner user ID")
    title: str = Field(..., description="Chapter title")
    chapter_number: int = Field(..., description="Sequence number")
    content: str = Field(..., description="Current working manuscript")
    original_content: str = Field(
        ...,
        description="Preserved immutable initial manuscript submitted by author",
    )
    word_count: int = Field(..., description="Word count of current manuscript")
    processing_status: ProcessingStatus = Field(
        default=ProcessingStatus.PENDING,
        description="Status of AI memory extraction and ingestion",
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error details if processing failed",
    )
    retry_count: int = Field(
        default=0,
        description="Number of times processing was retried",
    )
    created_at: datetime = Field(..., description="Chapter creation timestamp")
    updated_at: datetime = Field(..., description="Last updated timestamp")

    model_config = {"from_attributes": True}


class ChapterStatusResponse(BaseModel):
    """Lightweight response for checking processing status."""

    chapter_id: str
    story_id: str
    processing_status: ProcessingStatus
    retry_count: int
    error_message: Optional[str] = None
    message: str


class PaginatedChapterResponse(PaginatedResponse[ChapterResponse]):
    """Paginated list of chapters."""
    pass

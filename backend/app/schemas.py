from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


SkipReason = Literal[
    "not_my_field",
    "not_eligible",
    "hours",
    "pay",
    "not_interested",
    "other",
]


class CardIn(BaseModel):
    role: str
    company: str
    field: str
    source: str
    source_url: str
    students_ok: bool = True
    experience: str
    hours: str
    pay: str = ""
    deadline: str  # YYYY-MM-DD

    @field_validator("role", "company", "field", "source", "source_url", "experience", "hours", "deadline")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be blank")
        return v.strip()


class PublishRequest(BaseModel):
    cards: list[CardIn] = Field(min_length=5, max_length=5)


class PublishResponse(BaseModel):
    set_id: UUID
    card_count: int


class CardOut(BaseModel):
    id: UUID
    set_id: UUID
    position: int
    role: str
    company: str
    field: str
    source: str
    source_url: str
    students_ok: bool
    experience: str
    hours: str
    pay: str
    deadline: str


class CardSetOut(BaseModel):
    id: UUID
    published_at: str
    cards: list[CardOut]


class DecideRequest(BaseModel):
    set_id: UUID
    card_id: UUID
    position: int
    decision: Literal["apply", "skip"]
    skip_reason: SkipReason | None = None
    ms_on_card: int | None = None
    anonymous_id: str
    ms_total: int | None = None

    @field_validator("anonymous_id")
    @classmethod
    def anon_ok(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("anonymous_id required")
        return v.strip()


class AppliedSummary(BaseModel):
    role: str
    deadline: str
    source_url: str


class DecideResponse(BaseModel):
    ok: bool = True
    complete: bool
    summary: list[AppliedSummary] | None = None

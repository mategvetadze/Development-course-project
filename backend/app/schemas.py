from typing import Literal
from uuid import UUID
from datetime import date

from pydantic import BaseModel, Field, HttpUrl, TypeAdapter, field_validator


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

    @field_validator("deadline")
    @classmethod
    def valid_deadline(cls, v: str) -> str:
        if date.fromisoformat(v).isoformat() != v:
            raise ValueError("must be YYYY-MM-DD")
        return v

    @field_validator("source_url")
    @classmethod
    def valid_source_url(cls, v: str) -> str:
        TypeAdapter(HttpUrl).validate_python(v)
        return v


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
    position: int = Field(ge=1, le=5)
    decision: Literal["apply", "skip"]
    skip_reason: SkipReason | None = None
    ms_on_card: int | None = Field(default=None, ge=0, le=2147483647)
    anonymous_id: str
    ms_total: int | None = Field(default=None, ge=0, le=9007199254740991)

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
    decision: Literal["apply", "skip"]


class DecisionState(BaseModel):
    choices: dict[str, Literal["apply", "skip"]]
    complete: bool
    summary: list[AppliedSummary] | None = None

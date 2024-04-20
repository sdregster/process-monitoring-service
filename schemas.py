from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SProcessCreate(BaseModel):
    name: str


class SProcess(SProcessCreate):
    id: int
    started_at: datetime
    finished_at: Optional[datetime]
    notified: bool

    model_config = ConfigDict(from_attributes=True)


class SProcessId(BaseModel):
    ok: bool = True
    process_id: int


class SInfoAdd(BaseModel):
    process_id: int
    message: str


class SInfo(SInfoAdd):
    id: int


class SInfoId(BaseModel):
    ok: bool = True
    info_id: int

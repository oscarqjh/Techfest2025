from typing import Optional
from sqlmodel import SQLModel, Field, Text
from sqlalchemy.dialects.postgresql import JSONB

class RurlData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: str

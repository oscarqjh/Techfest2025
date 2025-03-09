from typing import Optional
from sqlmodel import SQLModel, Field

class CredibleSite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    domain: str
from typing import Optional
from sqlmodel import SQLModel, Field

class Website(SQLModel, table=True):
    wid: Optional[int] = Field(default=None, primary_key=True)
    url: str
    
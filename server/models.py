from pydantic import BaseModel

class TestAPIResponse(BaseModel):
    """TestAPIResponse schema."""
    message: str

class TestAPIRequest(BaseModel):
    """TestAPIRequest schema."""
    url: str


class ValidationAPIRequest(BaseModel):
    """ValidationAPIRequest schema."""
    url: str

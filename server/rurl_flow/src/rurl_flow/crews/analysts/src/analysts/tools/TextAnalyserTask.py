from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import LlmClient

"""
This is a tool that analyzes text content to determine its credibility and accuracy.

Returns:
    is_fake: bool
    confidence_score: float
    reason: str
"""

class TextEvaluationItem(BaseModel):
    """Schema for each evaluation item in the text analysis"""
    is_fake: bool
    confidence_score: float
    reason: str

class TextAnalyserInput(BaseModel):
    """Input schema for TextAnalyser"""
    data: dict

class TextAnalyserOutput(BaseModel):
    """Output schema for TextAnalyser"""
    evaluation: List[TextEvaluationItem]

class TextAnalyserTask(BaseTool):
    name: str = "TextAnalyser"
    description: str = "This tool analyses the content of a text to determine its credibility and accuracy."
    args_schema: Type[BaseModel] = TextAnalyserInput

    def _run(self, data: dict) -> dict:
        data = LlmClient.call_openai_api(data, "TextAnalyser")
        structured_data = TextAnalyserOutput(**data['text_analysis'])
        return structured_data.model_dump()
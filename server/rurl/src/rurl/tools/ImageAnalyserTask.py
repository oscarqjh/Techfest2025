from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import LlmClient

"""
This is a tool that analyzes images to determine their authenticity.
"""

class ImageEvaluationItem(BaseModel):
    """Schema for each evaluation item in the image analysis"""
    image_url: str
    is_fake: bool
    confidence_score: float
    reason: str

class ImageAnalyserInput(BaseModel):
    """Input schema for ImageAnalyser"""
    data: dict

class ImageAnalyserOutput(BaseModel):
    """Output schema for ImageAnalyser"""
    evaluation: List[ImageEvaluationItem]

class ImageAnalyserTask(BaseTool):
    name: str = "ImageAnalyser"
    description: str = "This tool analyzes the authenticity of images."
    args_schema: Type[BaseModel] = ImageAnalyserInput

    def _run(self, data: dict) -> dict:
        data = LlmClient.call_openai_api(data, "ImageAnalyser")
        structured_data = ImageAnalyserOutput(**data['image_analysis'])
        return structured_data.model_dump()
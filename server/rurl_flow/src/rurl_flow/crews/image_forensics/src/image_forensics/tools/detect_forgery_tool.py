from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai import LLM
from dotenv import load_dotenv

_ = load_dotenv()

class DetectForgeryToolInput(BaseModel):
    """Input schema for AnalyseNewsTool."""
    image_links: list[str] = Field(..., description="List of image paths to be analysed.")
    # Update with fields returned from the web_parser tool

class DetectForgeryToolOutput(BaseModel):
    """Output schema for AnalyseNewsTool."""
    classification: str = Field(..., description="Classification of the image. Either 'forged' or 'authentic'.")
    confidence: float = Field(..., description="Confidence score of the classification.")

class DetectForgeryTool(BaseTool):
    name: str = "Image Forgery Detection Tool"
    description: str = (
        "This tool receives an image and runs it through an image forgery detection model to determine if the image has been tampered with."
    )
    args_schema: Type[BaseModel] = DetectForgeryToolInput
    detection_model: str # Change to model class when implemented ie. 'ImageForgeryDetector'

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, detection_model: str):
        """Initializes the tool with the forgery detection model."""
        super().__init__(detection_model=detection_model)
        self.detection_model = detection_model

    def _run(self, image_links: list[str]) -> dict:
        # Implementation goes here
        # classification, confidence = self.detection_model.run(argument) # Replace with actual implementation of the forgery detection model
        classification = "forged"   # PLACEHOLDER
        confidence = 0.9            # PLACEHOLDER
        return {"classification": classification, "confidence": confidence}

if __name__ == "__main__":
    tool = DetectForgeryTool("Placeholder detection model")
    data = DetectForgeryToolInput(image_links=["Placeholder/placeholder.png"])
    print(tool.run(data))
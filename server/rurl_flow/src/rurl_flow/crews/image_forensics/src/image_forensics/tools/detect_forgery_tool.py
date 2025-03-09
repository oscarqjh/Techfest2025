from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai import LLM
from dotenv import load_dotenv

<<<<<<< HEAD
from PIL import Image # Module for image processing - Iain
from transformers import pipeline # Module for running models - Iain
import requests
from io import BytesIO

=======
>>>>>>> staging
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
<<<<<<< HEAD
    model: str = "umm-maybe/AI-image-detector" # Change to model class when implemented ie. 'ImageForgeryDetector'
    
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, detection_model: str = "umm-maybe/AI-image-detector"):
        """Initializes the tool with the forgery detection model."""
        super().__init__()
        self.model =pipeline("image-classification", detection_model) # Model - Iain

    def _run(self, image_links: list[str]) -> dict: 
        results = []
        for img_url in image_links:
            try:
                response = requests.get(img_url, timeout=10)  # Fetch image from URL
                response.raise_for_status()  # Raise error for bad response
                image = Image.open(BytesIO(response.content)).convert("RGB")  # Open image from memory
                
                # Run the model
                outputs = self.model(image)
                best_result = max(outputs, key=lambda x: x['score'])
                classification = best_result['label']
                confidence = best_result['score']
                
                results.append({"classification": classification, "confidence": confidence})
            except requests.exceptions.RequestException as e:
                results.append({"error": f"Failed to fetch image '{img_url}': {str(e)}"})
            except Exception as e:
                results.append({"error": str(e)})

        return results

if __name__ == "__main__":
    tool = DetectForgeryTool("umm-maybe/AI-image-detector")
=======
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
>>>>>>> staging
    data = DetectForgeryToolInput(image_links=["Placeholder/placeholder.png"])
    print(tool.run(data))
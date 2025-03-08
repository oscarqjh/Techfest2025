from .globals import client
import json

"""3 different api calls are defined here:
    1. WebAnalyser to see which para to factcheck
    2. ImageAnalyser to check if image is fake or real
    3. TextAnalyser to analyse if text is fake or real

example output
{'image_analysis': [{'evaluation': [{'image_url': 'https://example.com/image1.jpg', 
'is_fake': True, 'confidence_score': 0.2
'reason': 'The image shows a surreal scene with a giant hand controlling a cityscape, which is clearly manipulated and not realistic.'}]}], 
'text_analysis': {'evaluation': [{'is_fake': False, 'confidence_score': 0.65, 'reason': "The text presents a critical analysis of Singapore's sovereignty and its relationship with the U.S., but it shows bias against U.S. influence and lacks multiple viewpoints. It raises valid points but does not provide sufficient factual references to support all claims."}]}}
"""

response_format_web = {
    "type": "object",
    "properties": {
        "topic": {
            "type": "array",
            "items": {"type": "string"}
        },
        "article_body": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "content": {"type": "string"},
                    "to_fact_check": {"type": "boolean"}
                },
                "required": ["id", "content", "to_fact_check"]
            }
        }
    },
    "required": ["article_body", "topic"]
}

response_format_image = {
    "type": "object",
    "properties": {
        "evaluation": {
            "type": "object",  
            "properties": {
                "image_url": {"type": "string"},  # The image being evaluated
                "is_fake": {"type": "boolean"},   # True if fake, False if real
                "confidence_score": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "multipleOf": 0.1  # 1dp
                },
                "reason": {
                    "type": "string",  
                    "description": "Explanation of why the image was classified as fake or real"
                }
            },
            "required": ["image_url", "is_fake", "confidence_score", "reason"]
        }
    }
}

response_format_text = {
    "type": "object",
    "properties": {
        "evaluation": { 
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "is_fake": {"type": "boolean"},  # True if fake, False if real
                    "confidence_score": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "multipleOf": 0.1  # 1dp
                    },
                    "reason": {  
                        "type": "string",  
                        "description": "Explanation of why the text was classified as fake or real"
                    }
                },
                "required": ["is_fake", "confidence_score", "reason"]
            }
        }
    }
}

functions = [
    {
        "name": "WebAnalyser",
        "description": "Determine if each paragraph needs to be fact-checked",
        "parameters": response_format_web
    },
    {
        "name": "ImageAnalyser",
        "description": "Analyse the image(s) and return scores with explanation",
        "parameters": response_format_image
    },
    {
        "name": "TextAnalyser",
        "description": "Analyse the text and return scores with explanation",
        "parameters": response_format_text       
    }
]

def prepare_message(function_name, **kwargs):
    website_link = kwargs.get('weblink', '')
    
    if function_name == "WebAnalyser":
        title = kwargs.get('title', '')
        content = kwargs.get('content', '')
        
        return [
            {
                "role": "system",
                "content": """You are an expert in fact-checking web content and extracting key information.
                              You are given a webpage link and need to provide an analysis of the article body and identify paragraphs that need to be fact-checked."""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        Remember the following information.
                        
                        <Title>
                        This is the title of the webpage.
                        {title}
                        </Title>
                        
                        <Content>
                        This is the content of the webpage.
                        {content}
                        </Content>
                        
                        ### **Instructions:**
                        1. You are tasked with doing a paragraph level analysis of the content of the webpage.
                        2. For each paragraph, provide an ID, the content, and whether it needs to be fact-checked.
                        3. If a paragraph needs to be fact-checked, set the value of `to_fact_check` to `true`.
                                                
                        ### **Safeguards**
                        1. Start the id of the paragraph from 0, followed by 1, 2, etc.
                        2. Identify paragraphs that contain statements that are not supported by credible sources or lack proper references.
                        3. Look for paragraphs that present one-sided arguments or show clear bias without presenting multiple viewpoints.
                        4. Detect paragraphs that contain exaggerated claims or sensationalist language that may indicate misinformation.
                        5. Identify paragraphs that contradict known facts or established knowledge.
                        6. Look for paragraphs that contain logical fallacies or inconsistencies in the argumentation.
                        7. Detect paragraphs that use emotionally charged language to manipulate the reader's perception.
                        8. Analyse ALL paragraphs in the content provided.
                        9. For topic extraction, identify the main topics discussed in the article.
                        
                        ### **Example Output:**
                        The output will be:
                            {{
                              "type": "object",
                              "properties": {{
                                "article_body": [
                                  {{
                                    "id": "1",
                                    "content": "This is the first paragraph.",
                                    "to_fact_check": false
                                  }},
                                  {{
                                    "id": "2",
                                    "content": "This is the second paragraph.",
                                    "to_fact_check": true
                                  }}
                                ],
                                "topic": ["climate change", "food security", "global impact"]
                              }},
                              "required": ["article_body", "topic"]
                            }}
                        """
                    }
                ]
            }
        ]

    if function_name == "ImageAnalyser":
        image = kwargs.get('image')

        return [
            {
                "role": "system",
                "content": """You are an expert in analyzing images and determining whether they are real or fake. 
                              You are given a list of image(s) and you need to evaluate them using reasoning."""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        You are an AI trained to assess the authenticity of images. Your task is to evaluate the image based on the following criteria and assign a **realness score** from **0 to 1** where:
                        - **0** indicates "Fake" or "Manipulated"
                        - **1** indicates "Authentic" or "Real"

                        The score should be given with **two decimal points** (e.g., 0.92) based on the following rubric:

                        ### **1. Source Verification (25%)**
                        - **Score: 0–1**
                          - **1**: The image is from a credible source (e.g., verified news organizations, official social media accounts, trustworthy repositories).
                          - **0.5**: The source is unverified or comes from unreliable platforms (e.g., memes, viral websites).
                          - **0**: The source is questionable or from an untrustworthy domain (e.g., conspiracy websites, unverified social media accounts).

                        ### **2. Image Quality & Resolution (25%)**
                        - **Score: 0–1**
                          - **1**: The image has high resolution and clarity, with no visible distortions or artifacts.
                          - **0.5**: The image quality is moderate, with some visible artifacts or low resolution, but no major distortions.
                          - **0**: The image is heavily pixelated, blurry, or contains visual distortions indicating manipulation.

                        ### **3. Context Consistency (25%)**
                        - **Score: 0–1**
                          - **1**: The image fits within its context and aligns with known facts or events (e.g., news event, historical records).
                          - **0.5**: The image context is partially inconsistent with known facts but could still be plausible.
                          - **0**: The image is completely inconsistent with the given context or contradicts verified facts (e.g., wrong location, time, or event).

                        ### **4. Image Manipulation (25%)**
                        - **Score: 0–1**
                          - **1**: No signs of manipulation detected (e.g., no unusual artifacts, consistent lighting, no evident Photoshop usage).
                          - **0.5**: Minor signs of manipulation (e.g., small discrepancies in shadows, lighting, or image stitching).
                          - **0**: Clear signs of manipulation (e.g., mismatched lighting, unnatural shadows, or suspicious edits).

                        ### **Final Score Calculation**:
                        - Calculate the final **realness score** by summing the weighted scores from each category.
                        - **Example Final Calculation**: 
                          - Source Verification: 0.9 (weighted 20%) = 0.18
                          - Image Quality: 0.8 (weighted 20%) = 0.16
                          - Context Consistency: 1.0 (weighted 20%) = 0.20
                          - Image Manipulation: 0.4 (weighted 20%) = 0.08
                          - **Final Score = 0.18 + 0.16 + 0.20 + 0.08 = 0.62**

                        The **realness score** will range from **0 (Fake)** to **1 (Real)**.

                        ### **Instructions:**
                        1. Carefully evaluate the image on all five criteria.
                        2. Provide a score between **0 and 1** for each category.
                        3. Sum the weighted scores and round to two decimal places to get the final realness score.
                        4. Provide a short explanation for each criterion to justify your score.

                        **Please ensure that the overall analysis is fair, detailed, and justified based on the image's content and metadata.**
                        
                        ---
                        
                        ### **Example Output:**
                        The output will be
                            {{
                              "type": "array",
                              "items": [
                                {{
                                  "image_url": "https://example.com/image1.jpg",
                                  "is_fake": true,
                                  "confidence_score": 0.8,
                                  "reason": "The image contains unusual lighting and inconsistent shadows, which suggests manipulation."
                                }}
                              ]
                            }}

                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {  
                            "url": image
                        }
                    }                    
                ]
            
            }
        ]
    
    if function_name == "TextAnalyser":
        text = kwargs.get('text', '')
        title = kwargs.get('title', '')
        date = kwargs.get('date', '')
        weblink = kwargs.get('weblink', '')
        
        return [
            {
                "role": "system",
                "content": """You are an expert in analyzing text and determining whether it is real or fake.
                              You are given a text content and you need to evaluate it using reasoning based on the following rubrics and assign a score from 0 to 1.
                              The score should be provided with two decimal points (e.g., 0.92)."""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        Instructions:

                        Remember the following information.

                        <Objective>
                        1 Taking into account the following rubrics, evaluate the text content.
                        </Objective>

                        <Title>
                        2. The title of the text: {title}
                        </Title>
                        
                        <Content>
                        3. The content to be evaluated: {text}
                        </Content>

                        <Rubric>
                        4. Please evaluate the text based on the following rubrics:

                        ### **1. Source Credibility (20%)**
                        - **Score: 0-1**
                        - **1**: The source is highly credible (e.g., verified news organizations, academic papers).
                        - **0.5**: The source is somewhat credible (e.g., blog posts, unverified social media).
                        - **0**: The source is untrustworthy (e.g., conspiracy sites, unreliable sources).

                        ### **2. Objectivity (25%)**
                        - **Score: 0-1**
                        - **1**: The text is objective, without visible bias or subjective tone.
                        - **0.5**: The text has some bias but presents multiple viewpoints.
                        - **0**: The text is highly biased, with one-sided arguments and no balance.

                        ### **3. Factual Accuracy (25%)**
                        - **Score: 0-1**
                        - **1**: The text contains accurate, well-researched, and verifiable facts.
                        - **0.5**: The text contains some factual inaccuracies or lacks proper references.
                        - **0**: The text is mostly false or misleading with no factual support.

                        ### **4. Writing Quality (15%)**
                        - **Score: 0-1**
                        - **1**: The text is well-written, clear, and free from spelling or grammatical errors.
                        - **0.5**: The text has minor spelling or grammatical issues.
                        - **0**: The text contains significant spelling or grammatical issues.

                        ### **5. Manipulation Signs (15%)**
                        - **Score: 0-1**
                        - **1**: No signs of manipulation or exaggerated claims.
                        - **0.5**: The text has some exaggerated claims or misleading information but no manipulation.
                        - **0**: The text is manipulated or contains misleading information intended to deceive.

                        ### **Final Score Calculation:**
                        - Calculate the final score by summing the weighted scores from each category.
                        - For example, if Source Credibility = 0.9, Objectivity = 0.7, Factual Accuracy = 0.8, Writing Quality = 1.0, and Manipulation Signs = 0.6, the final score would be:
                            - **Final Score = (0.9 * 0.20) + (0.7 * 0.25) + (0.8 * 0.25) + (1.0 * 0.15) + (0.6 * 0.15) = 0.82**

                        5. Please provide a **final score** between **0 and 1** with **two decimal points**.
                        </Rubric>

                        ---

                        ### **Example Output:**
                        The output will be:
                            {{
                              "evaluation": [
                                {{
                                  "is_fake": false,
                                  "confidence_score": 0.95,
                                  "reason": "The text comes from a reputable environmental journal and is based on verifiable facts."
                                }},
                              ]
                            }}
                        """
                    }
                ]
            }
        ]
        
def call_openai_api(data, function_name): 
    title = data['data']['title']
    weblink = data['data']['weblink']
    images = data['data']['image_url']
    text = data['data']['content']
    date = data['data']['date']
    
    output = {}  # Store both image and text results
    if function_name == "WebAnalyser":
        model = 'gpt-4o-mini'
        messages = prepare_message(title=title, content=text, function_name="WebAnalyser")
        
        try:
            response = client.chat.completions.create(
                model=model,  
                messages=messages,
                functions=functions,
                function_call={"name": "WebAnalyser"},
                temperature=0.1
            )
            function_args = response.choices[0].message.function_call.arguments
            web_data = json.loads(function_args)
            
            output["web_analysis"] = web_data  # Store web analysis results
        
        except Exception as e:
            print(f"Error occurred while calling OpenAI API for web content: {e}")
            
    if function_name == "ImageAnalyser":
        if images:
            image_output = []
            model = 'gpt-4o'
            
            try:
                for image in images:
                    messages = prepare_message(
                        title=title, 
                        weblink=weblink, 
                        image=image,  
                        text=text, 
                        function_name="ImageAnalyser"
                    )
                    response = client.chat.completions.create(
                        model=model,  
                        messages=messages,
                        functions=functions,
                        function_call={"name": "ImageAnalyser"},
                        temperature=0.1
                    )
                    function_args = response.choices[0].message.function_call.arguments
                    image_data = json.loads(function_args)
                    image_output.append(image_data)
                
                output["image_analysis"] = image_output  # Store image analysis results
            
            except Exception as e:
                print(f"Error occurred while calling OpenAI API for images: {e}")

    if function_name == "TextAnalyser":
        if text:
            model = 'gpt-4o-mini'
            
            try:
                messages = prepare_message(title=title, text=text, date=date, weblink=weblink, function_name="TextAnalyser")
                response = client.chat.completions.create(
                    model=model,  
                    messages=messages,
                    functions=functions,
                    function_call={"name": "TextAnalyser"},
                    temperature=0.1
                )
                function_args = response.choices[0].message.function_call.arguments
                text_data = json.loads(function_args)

                output["text_analysis"] = text_data  # Store text analysis results
            
            except Exception as e:
                print(f"Error occurred while calling OpenAI API for text: {e}")

    if output:
        return output
    
    else:
        print("No valid input provided for either text or images.")
        return None

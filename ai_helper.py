import os
import json
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def analyze_plant_disease(image_bytes):
    """
    Analyze plant image for disease detection using AI vision
    Returns detailed information about plant health, diseases, treatments
    """
    if not openai_client:
        return {
            "error": "AI service not configured. Please add your OpenAI API key.",
            "disease_name": "Service Unavailable",
            "confidence": 0,
            "severity": "Unknown",
            "symptoms": "AI analysis requires API key configuration.",
            "causes": "No analysis available",
            "treatment": "Please configure OpenAI API key to use disease detection.",
            "prevention": "Configure API key in settings",
            "recommended_products": []
        }
    
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """You are an expert agricultural pathologist. Analyze this plant image and provide a detailed diagnosis in JSON format.

Respond with a JSON object containing:
{
    "plant_type": "name of the plant if identifiable",
    "disease_name": "specific disease name or 'Healthy' if no disease detected",
    "confidence": confidence score from 0.0 to 1.0,
    "severity": "Low", "Medium", "High", or "Critical",
    "symptoms": "detailed description of visible symptoms",
    "causes": "what causes this disease (environmental, fungal, bacterial, viral, etc.)",
    "treatment": "detailed treatment recommendations including specific actions",
    "prevention": "prevention measures to avoid this disease in future",
    "recommended_products": ["list of 3-5 specific agricultural products/medications that can treat this"]
}

Be specific and professional. If the image is not a plant, indicate that clearly."""

        response = openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2048
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "disease_name": "Analysis Error",
            "confidence": 0,
            "severity": "Unknown",
            "symptoms": f"Error during analysis: {str(e)}",
            "causes": "Unable to analyze",
            "treatment": "Please try again or consult an expert",
            "prevention": "Ensure good image quality",
            "recommended_products": []
        }

def get_agricultural_advice(question, context=""):
    """
    Get AI-powered agricultural advice and recommendations
    """
    if not openai_client:
        return "AI assistant is not configured. Please add your OpenAI API key to use this feature."
    
    try:
        system_prompt = """You are an expert agricultural advisor with extensive knowledge in:
- Crop cultivation and management
- Plant diseases and pest control
- Soil health and fertilization
- Irrigation and water management
- Organic and sustainable farming practices
- Weather-related crop planning
- Harvest timing and post-harvest handling

Provide practical, actionable advice to farmers. Be specific, clear, and helpful."""

        user_message = question
        if context:
            user_message = f"Context: {context}\n\nQuestion: {question}"

        response = openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_completion_tokens=1024
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error getting advice: {str(e)}"

def search_product_images(product_name):
    """
    Generate or find product images for medications/treatments
    This is a placeholder - in production, you'd integrate with a product database
    """
    return f"https://via.placeholder.com/300x200?text={product_name.replace(' ', '+')}"

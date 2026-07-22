from google import genai 
import os 

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_comparison_summary(city1_data : dict , city2_data : dict) :
    prompt = f"""
    Compare these two Indian cities for someone deciding where to live.
    City 1: {city1_data}
    City 2: {city2_data}
    Give a short, clear paragraph on which is better and why,
    covering cost, safety, air quality and healthcare.
    """
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text

async def generate_recommendation(preferences: str, cities_data: list):
    prompt = f"""
    User preferences: {preferences}
    Available cities data: {cities_data}
    Recommend the single best-fit city and explain why in 2-3 sentences.
    """
    response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
    )
    return response.text
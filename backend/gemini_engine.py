from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_strategy(prob, risk):
    try:
        prompt = f"""
You are a Netflix senior business strategist.

User churn probability: {prob:.2f}
Risk level: {risk}

Generate exactly 3 HIGH-QUALITY retention strategies.

Rules:
- No generic suggestions
- Focus on Netflix streaming business
- Make them actionable

Return bullet points.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",   # 🔥 YOUR TARGET MODEL
            contents=prompt
        )

        text = response.text.strip()

        strategies = [
            s.replace("-", "").strip()
            for s in text.split("\n")
            if s.strip()
        ]

        return strategies[:3]

    except Exception as e:
        print("🔥 GEMINI ERROR:", e)
        return [
            "Offer personalized content recommendations",
            "Provide retention discounts",
            "Send targeted re-engagement notifications"
        ]
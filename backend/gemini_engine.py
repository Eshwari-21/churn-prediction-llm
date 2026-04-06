import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_strategy(prob, risk):
    try:
        prompt = f"""
        You are a Netflix business analyst.

        Churn probability: {prob:.2f}
        Risk level: {risk}

        Give 3 short actionable strategies to retain the user.

        Return only bullet points.
        """

        response = model.generate_content(prompt)
        text = response.text.strip()

        strategies = [
            line.replace("-", "").replace("•", "").strip()
            for line in text.split("\n")
            if line.strip()
        ]

        return strategies[:3]

    except Exception as e:
        print("LLM ERROR:", e)

        # fallback (still looks like LLM output)
        return [
            "Offer personalized recommendations",
            "Send targeted re-engagement notifications",
            "Provide loyalty incentives"
        ]
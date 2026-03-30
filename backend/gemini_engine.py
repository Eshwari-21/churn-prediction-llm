from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_strategy(data, prob, risk):

    prompt = f"""
    A Netflix user has churn probability {prob} (Risk: {risk}).

    Generate exactly 3 retention strategies.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Gemini Error:", e)

        # 🔥 HANDLE QUOTA ERROR
        if "429" in str(e):
            time.sleep(4)   # wait before retry

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                return response.text
            except:
                pass

        # 🔥 FINAL FALLBACK (only if quota exceeded)
        return """1. Offer personalized discount
2. Recommend trending content
3. Improve engagement via notifications"""
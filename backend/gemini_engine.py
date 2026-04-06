
from google import genai

# 🔥 PUT YOUR REAL API KEY
client = genai.Client(api_key="AIzaSyDD3OhLZgae-XHKaEZC1gwf7I3lkePRcM4")
def generate_strategy(data, prob, risk):
    try:
        prompt = f"""
        Customer churn probability: {prob}
        Risk: {risk}
        Data: {data}

        Suggest 3 short retention strategies.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text

        if not text:
            raise Exception("Empty response")

        strategies = [
            line.replace("-", "").strip()
            for line in text.split("\n")
            if line.strip()
        ]

        return strategies[:3]

    except Exception as e:
        print("LLM ERROR:", e)

        # fallback (VERY IMPORTANT)
        return [
            "Offer discount",
            "Send personalized recommendations",
            "Provide loyalty rewards"
        ]
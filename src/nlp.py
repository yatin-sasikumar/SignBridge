from dotenv import load_dotenv
import os
import cohere

load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

co = cohere.Client(api_key)

def refine_text(words):
    raw = " ".join(words)

    prompt = f"""
    Convert this sign language output into a natural, grammatically correct English sentence.

    Input: "{raw}"

    i dont need explaination or stuff, just get me the sentence also if there is smtng irrelevant to the sentence like the phrase "I love you" or if there redudancies, remove them
    """

    try:
        response = co.chat(
           
            message=prompt
        )

        return response.text.strip()

    except Exception as e:
        print("Cohere failed:", e)

        # 🔥 fallback
        return raw.lower().capitalize()
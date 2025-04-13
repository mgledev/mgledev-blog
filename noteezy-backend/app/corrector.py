import openai
import os

def correct_text(text, language="pl"):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Popraw poniższy tekst ({language}):\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
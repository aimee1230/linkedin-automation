import json
import ollama


def generate_keywords(profile):

    text = f"""
Profile About:
{profile.get("about", "")}
"""

    try:
        response = ollama.chat(
            model="qwen3.5:0.8b",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at generating LinkedIn search keywords.

Your job is to return ONLY valid JSON output.

Rules:
- Output must be a JSON list of exactly 10 strings
- Each keyword must be 1 to 3 words
- No explanations, no extra text
- No numbering
- No duplicate keywords
- Focus on professional and technical topics
"""
                },
                {
                    "role": "user",
                    "content": f"""
Generate 10 LinkedIn search keywords based on this profile.

Profile:
{text}

Return ONLY JSON.

Example:
["machine learning","computer vision","ai research","deep learning","nlp"]
"""
                }
            ]
        )

        output = response["message"]["content"].strip()

        # Clean output (important for small models)
        if "[" in output:
            output = output[output.find("["):]

        keywords = json.loads(output)

        # Safety check
        if not isinstance(keywords, list):
            raise ValueError("Not a list")

        print("Generated keywords:", keywords)

        return keywords

    except Exception as e:
        print("Keyword generation failed:", e)
        print("Raw output:", output if 'output' in locals() else "")

        # fallback
        return ["machine learning", "ai", "data science"]
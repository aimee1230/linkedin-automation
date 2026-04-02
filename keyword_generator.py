import json
import ollama


def generate_keywords(profile):
    text = f"""
Profile About:
{profile.get("about","")}
"""

    prompt = f"""
You are generating LinkedIn search keywords.

Based on the profile below, generate 10 SHORT keywords
that would be used to search LinkedIn posts.

Rules:
- 1 to 3 words per keyword
- Must match the person's profession or expertise
- Avoid generic topics like "career growth"
- Avoid marketing terms
- Focus on technical or professional topics

Return ONLY a valid JSON list.

Example:
["machine learning","computer vision","ai research","deep learning","nlp"]

Profile:
{text}

JSON Output:
["""

    try:
        # Using the official ollama python library
        response = ollama.chat(
            model="qwen3.5:0.8b",
            messages=[{"role": "user", "content": prompt}],
            think=False,  
            options={
                "temperature": 0.1,  # Keep it hyper-focused
                "stop": ["]\n"],  # Stop generating the moment the array closes
            },
        )

        output = response.message.content.strip()

        # Since we pre-filled the prompt with '[', let's ensure it has the bracket before parsing
        if not output.startswith("["):
            output = "[" + output

        # Parse the JSON output
        keywords = json.loads(output)
        print("Generated keywords:", keywords)
        return keywords

    except Exception as e:
        print("Keyword generation failed")
        print(f"Error: {e}")
        return []
import subprocess
import json


def run_llm(prompt):

    result = subprocess.run(
        [
            "ollama",
            "run",
            "qwen2.5:3b",
            prompt
        ],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


def generate_keywords(profile):

    text = f"""
Profile Headline:
{profile.get("headline","")}

Profile About:
{profile.get("about","")}
"""

    prompt = f"""
You are generating LinkedIn search keywords.

Based on the profile below, generate 5 SHORT keywords
that would be used to search LinkedIn posts.

Rules:
- 1 to 3 words per keyword
- Must match the person's profession or expertise
- Avoid generic topics like "career growth"
- Avoid marketing terms
- Focus on technical or professional topics

Return ONLY a JSON list.

Example:
["machine learning","computer vision","ai research","deep learning","nlp"]

Profile:
{text}
"""
    output = run_llm(prompt)

    try:
        keywords = json.loads(output)

        print("Generated keywords:", keywords)

        return keywords

    except:
        print("Keyword generation failed")
        print(output)
        return []
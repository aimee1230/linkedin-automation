def comment_prompt(post_text):

    return f"""
Write a thoughtful LinkedIn comment based on the content below.

The input may include:
- Post text
- One or more images

IMPORTANT:
- If the post is about hiring, job openings, recruitment, or "we are hiring", return EXACTLY: SKIP
- Do NOT generate a comment for hiring-related posts

Instructions:
- Use both the text and images (if available) to understand the context
- Focus on the main idea or insight of the post
- Add a meaningful observation, perspective, or takeaway
- Keep it natural and human (like a real LinkedIn user)
- Maximum 2 sentences (prefer 1 strong sentence if possible)
- Avoid generic responses like "Great post", "Amazing", etc.
- Avoid emojis and hashtags
- Avoid promotional or marketing language
- Optionally include a short question ONLY if it adds value

Output Rules:
- Return ONLY the final comment
- No explanations, no extra text
- If hiring-related → return ONLY: SKIP

Post:
{post_text}
"""
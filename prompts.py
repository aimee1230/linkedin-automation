def comment_prompt(post_text):

    return f"""
Write a concise and meaningful LinkedIn comment about the post below.

The input may contain:
- Post text
- One image or multiple images

Instructions:
- If images are available, use them together with the text to understand context
- If no images are available, rely only on the text
- Focus on the main idea of the post
- Add one thoughtful insight, observation, or takeaway
- Do not repeat the post content

Rules:
- The comment MUST be 1 or 2 complete sentences
- Maximum 40 words
- Avoid generic praise (e.g., "Great post", "Nice", "Well said")
- No emojis, hashtags, or promotional language
- Optional: one short question only if it adds value
- Ensure the response is complete and not cut off
- Do not write lists or multiple paragraphs

Output:
Return ONLY the final comment.

Post:
{post_text}
"""
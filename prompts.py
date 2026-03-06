def comment_prompt(post_text):

    return f"""
Write a thoughtful LinkedIn comment responding to this post.

Rules:
- sound natural
- add insight or perspective
- max 2 sentences
- avoid promotion
- optionally include a short question

Post:
{post_text}
"""
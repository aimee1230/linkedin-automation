def comment_prompt(post_text):

    return f"""
Write a thoughtful LinkedIn comment responding to the post below.

Rules:
- sound natural and human
- add a small insight or perspective
- maximum 2 sentences
- avoid promotion or marketing language
- optionally include a short question if required to increase engagement
- do NOT include explanations, notes, or meta comments
- output ONLY the comment text

Post:
{post_text}
"""
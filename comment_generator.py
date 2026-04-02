import json
import os
from datetime import datetime

import ollama
from prompts import comment_prompt
from image_utils import download_image, delete_image


JSON_FILE = "processed_posts.json"


# -----------------------------------
# Generate comment using Ollama (MULTIMODAL)
# -----------------------------------
def generate_comment_with_ollama(post_text, image_paths=None):

    prompt = comment_prompt(post_text)

    content = [
        {"type": "text", "text": prompt}
    ]

    # Add multiple images if available
    if image_paths:
        for path in image_paths:
            content.append({
                "type": "image",
                "image": path
            })

    try:
        response = ollama.chat(
            model="qwen3.5:0.8b",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        print("Ollama error:", e)
        return None


# -----------------------------------
# Load JSON memory
# -----------------------------------
def load_memory():

    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, "r") as f:
        return json.load(f)


# -----------------------------------
# Save JSON memory
# -----------------------------------
def save_memory(data):

    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------
# Check / generate comment
# -----------------------------------
def get_or_generate_comment(post):

    memory = load_memory()
    post_id = post["id"]

    # -----------------------------
    # Check if already processed
    # -----------------------------
    for item in memory:
        if item["post_id"] == post_id:
            print("Post already processed. Skipping.")
            return None

    # -----------------------------
    # IMAGE HANDLING
    # -----------------------------
    image_paths = []

    image_urls = post.get("image_urls", [])

    for url in image_urls:
        path = download_image(url)
        if path:
            image_paths.append(path)

    # -----------------------------
    # Generate comment (MULTIMODAL)
    # -----------------------------
    comment = generate_comment_with_ollama(
        post["text"],
        image_paths
    )

    # -----------------------------
    # Cleanup image
    # -----------------------------
    for path in image_paths:
        delete_image(path)

    # -----------------------------
    # Save post data
    # -----------------------------
    post_entry = {
        "post_id": post["id"],
        "post_text": post["text"],
        "time": post["date"],
        "likes": post["likes"],
        "comments": post["comments"],
        "reposts": post["reposts"],
        "generated_comment": comment,
        "timestamp": datetime.now().isoformat()
    }

    memory.append(post_entry)
    save_memory(memory)

    return comment
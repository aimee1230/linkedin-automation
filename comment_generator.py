from datetime import datetime
import json
import os
import ollama
from prompts import comment_prompt


JSON_FILE = "processed_posts.json"


# -----------------------------------
# Generate comment using Ollama (MULTIMODAL)
# -----------------------------------
def generate_comment_with_ollama(post_text, image_paths=None):

    prompt = comment_prompt(post_text)
    message = {"role": "user", "content": prompt}

    if image_paths:
        message["images"] = image_paths

    try:
        response = ollama.chat(
            model="qwen3.5:0.8b",
            messages=[message],
            think=False,  # Stops Qwen from overthinking!
            options={
                "temperature": 0.3,  # Raised slightly to give it a bit more natural flow, but still low enough to prevent rambling
                "num_predict": 60,  # Lowered to 60 tokens so it CANNOT write a massive wall of text
            },
        )

        return response.message.content.strip()

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
        # Check if the URL is actually a local file on your machine
        if os.path.exists(url):
            image_paths.append(url)
        # If it's a web link, we'll import and use your image_utils
        elif url.startswith("http://") or url.startswith("https://"):
            try:
                from image_utils import download_image

                path = download_image(url)
                if path:
                    image_paths.append(path)
            except ImportError:
                print(
                    "image_utils not found. Skipping web download for this test."
                )
        else:
            print(f"Skipping invalid URL or unresolvable path: {url}")

    # -----------------------------
    # Generate comment (MULTIMODAL)
    # -----------------------------
    comment = generate_comment_with_ollama(post["text"], image_paths)

    # -----------------------------
    # Cleanup image (Only delete if it was a downloaded temp file!)
    # -----------------------------
    for path in image_paths:
        try:
            from image_utils import delete_image

            delete_image(path)
        except:
            pass

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
        "timestamp": datetime.now().isoformat(),
    }

    memory.append(post_entry)
    save_memory(memory)

    return comment
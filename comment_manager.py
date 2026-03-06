import json
import os
import subprocess
from datetime import datetime

from prompts import comment_prompt


JSON_FILE = "processed_posts.json"


# -----------------------------------
# Generate comment using OpenClaw
# -----------------------------------
def generate_comment_with_openclaw(post_text):

    prompt = comment_prompt(post_text)

    result = subprocess.run(
        [
            "openclaw",
            "agent",
            "--agent",
            "linkedin",
            "--message",
            prompt
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("OpenClaw error:", result.stderr)
        return None

    return result.stdout.strip()

# -----------------------------------
# Generate comment using Ollama
# -----------------------------------
def generate_comment_with_ollama(post_text):

    prompt = comment_prompt(post_text)

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

    if result.returncode != 0:
        print("Ollama error:", result.stderr)
        return None

    return result.stdout.strip()


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
    # Check if post already exists
    # -----------------------------
    for item in memory:

        if item["post_id"] == post_id:

            print("Post already processed. Skipping.")

            return None


    # -----------------------------
    # Generate comment
    # -----------------------------
    comment = generate_comment_with_openclaw(post["text"])


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
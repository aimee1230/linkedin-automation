import requests
import os
import uuid


# -----------------------------------
# Download image to current directory
# -----------------------------------
def download_image(image_url):

    if not image_url:
        return None

    try:
        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.jpg"

        # Save in current working directory
        filepath = os.path.join(os.getcwd(), filename)

        # Download image
        response = requests.get(image_url, timeout=5)

        if response.status_code != 200:
            return None

        # Write image to file
        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath

    except Exception as e:
        print("Image download failed:", e)
        return None


# -----------------------------------
# Delete image from current directory
# -----------------------------------
def delete_image(image_path):

    try:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
    except Exception as e:
        print("Image deletion failed:", e)
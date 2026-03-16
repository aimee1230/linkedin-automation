from linkedin_feed_reader import (
    start_browser,
    open_linkedin,
    scan_visible_posts,
    scroll_feed,
    scroll_top,
    wait_for_posts
)

from linkedin_comment_bot import post_comment
from trending_detector import calculate_score
from comment_generator import get_or_generate_comment
from config import POSTS_TO_SCAN, TRENDING_THRESHOLD, SCAN_DELAY_MIN, SCAN_DELAY_MAX

from profile_reader import extract_profile_data
from keyword_generator import generate_keywords
from keyword_memory import load_keywords
from keyword_search import open_keyword_search

import json
import os
import time
import random


JSON_FILE = "processed_posts.json"


# -----------------------------------
# Load processed post IDs
# -----------------------------------
def load_processed_ids():

    if not os.path.exists(JSON_FILE):
        return set()

    with open(JSON_FILE, "r") as f:
        data = json.load(f)

    return {item["post_id"] for item in data}


def run_agent():

    # -----------------------------------
    # Start browser
    # -----------------------------------
    start_browser()

    # -----------------------------------
    # Login to LinkedIn
    # -----------------------------------
    open_linkedin()

    print("Login manually if required...")
    time.sleep(20)

    # -----------------------------------
    # Profile Analysis
    # -----------------------------------
    print("\nAnalyzing profile...")
    profile = extract_profile_data()

    if not profile:
        print("Profile extraction failed.")
        return

    # -----------------------------------
    # Load or generate keywords
    # -----------------------------------
    keywords = load_keywords()

    if not keywords:
        keywords = generate_keywords(profile)

    if not keywords:
        print("\nNo keywords were generated.")
        return

    print("\nKeywords:", keywords)
    print("\nLinkedIn Keyword Agent Running...\n")

    # -----------------------------------
    # Load commented posts memory
    # -----------------------------------
    processed_ids = load_processed_ids()

    # -----------------------------------
    # Main Loop
    # -----------------------------------
    while True:

        for keyword in keywords:

            print(f"\nSearching posts for keyword: {keyword}")

            open_keyword_search(keyword)

            if not wait_for_posts():
                print("Posts did not load. Skipping keyword.")
                continue

            scanned = 0

            while scanned < POSTS_TO_SCAN:

                posts = scan_visible_posts()

                if not posts:
                    scroll_feed()
                    continue

                new_post_found = False

                for post in posts:

                    post_id = post["id"]

                    # -----------------------------------
                    # Skip already commented posts
                    # -----------------------------------
                    if post_id in processed_ids:
                        continue

                    new_post_found = True
                    scanned += 1

                    print(f"\nScanning Post {scanned}")

                    score = calculate_score(post)

                    if score >= TRENDING_THRESHOLD:

                        comment = get_or_generate_comment(post)

                        if comment:

                            post_comment(post_id, comment)

                            processed_ids.add(post_id)

                            print("\n==============================")
                            print("TRENDING POST FOUND")
                            print("==============================")

                            print("Keyword:", keyword)
                            print("Score:", score)
                            print("ID:", post_id)
                            print("Likes:", post["likes"])
                            print("Comments:", post["comments"])
                            print("Reposts:", post["reposts"])

                            print("\nText:\n", post["text"])
                            print("\nComment:", comment)

                    if scanned >= POSTS_TO_SCAN:
                        break

                # -----------------------------------
                # Stop scrolling if no new posts found
                # -----------------------------------
                if not new_post_found:
                    print("\nNo more new posts found. Stopping scroll.")
                    break

                scroll_feed()

            print(f"\nFinished scanning keyword: {keyword}")

            scroll_top()

            time.sleep(
                random.uniform(SCAN_DELAY_MIN, SCAN_DELAY_MAX)
            )


if __name__ == "__main__":
    run_agent()
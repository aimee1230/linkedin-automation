from extract import (
    start_browser,
    open_linkedin,
    scan_visible_posts,
    scroll_feed,
    scroll_top,
    wait_for_posts
)

from comment_poster import post_comment
from analyze import calculate_score
from comment_manager import get_or_generate_comment
from config import POSTS_TO_SCAN, TRENDING_THRESHOLD, SCAN_DELAY_MIN, SCAN_DELAY_MAX

from profile_extractor import open_profile, extract_profile_data
from keyword_generator import generate_keywords
from keyword_memory import save_keywords, load_keywords
from keyword_search import open_keyword_search

import time
import random


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

    open_profile()

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
        #save_keywords(keywords)

    # -----------------------------------
    # NEW CHECK
    # -----------------------------------
    if not keywords or len(keywords) == 0:
        print("\nNo keywords were generated from the profile.")
        print("Please check the profile content or keyword generation logic.")
        print("Stopping agent.")
        return

    print("\nKeywords:", keywords)

    print("\nLinkedIn Keyword Agent Running...\n")

    processed_ids = set()

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

                for post in posts:

                    if post["id"] in processed_ids:
                        continue

                    processed_ids.add(post["id"])

                    scanned += 1

                    print(f"\nScanning Post {scanned}")

                    score = calculate_score(post)

                    if score >= TRENDING_THRESHOLD:

                        comment = get_or_generate_comment(post)

                        post_comment(post["id"], comment)

                        print("\n==============================")
                        print("TRENDING POST FOUND")
                        print("==============================")

                        print("Keyword:", keyword)
                        print("Score:", score)
                        print("ID:", post["id"])
                        print("Likes:", post["likes"])
                        print("Comments:", post["comments"])
                        print("Reposts:", post["reposts"])

                        print("\nText:\n", post["text"])
                        print("\nComment:", comment)

                    if scanned >= POSTS_TO_SCAN:
                        break

                scroll_feed()

            print(f"\nFinished scanning keyword: {keyword}")

            scroll_top()

            time.sleep(
                random.uniform(SCAN_DELAY_MIN, SCAN_DELAY_MAX)
            )

def run():

    # -----------------------------------
    # Start browser
    # -----------------------------------
    print("\nStarting browser...")

    start_browser()


    # -----------------------------------
    # Open LinkedIn
    # -----------------------------------
    print("\nOpening LinkedIn...")

    open_linkedin()

    print("Please login manually if required.")
    time.sleep(20)


    # -----------------------------------
    # Open profile
    # -----------------------------------
    print("\nOpening profile page...")

    open_profile()

    time.sleep(5)


    # -----------------------------------
    # Extract profile data
    # -----------------------------------
    print("\nExtracting profile information...")

    profile = extract_profile_data()
    if not profile:
        print("Profile extraction failed. Exiting.")
        return
    print("\nTest finished. Exiting.")
    
if __name__ == "__main__":
    run()
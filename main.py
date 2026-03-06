from extract import (
    start_browser,
    open_linkedin,
    wait_for_feed,
    scan_feed,
    scroll_feed,
    scroll_top
)

from comment_poster import post_comment
from analyze import calculate_score
from comment_manager import get_or_generate_comment
from config import POSTS_TO_SCAN, TRENDING_THRESHOLD, SCAN_DELAY_MIN, SCAN_DELAY_MAX

import time
import random


def run_agent():

    start_browser()

    open_linkedin()

    wait_for_feed()

    print("LinkedIn Feed Agent Running...\n")

    while True:

        scanned = 0
        index = 0

        while scanned < POSTS_TO_SCAN:

            post = scan_feed(index)
            # If post not loaded yet → scroll
            if post is None:
                scroll_feed()
                continue

            scanned += 1

            print(f"\nScanning Post {scanned}")

            score = calculate_score(post)

            if score >= TRENDING_THRESHOLD:

                comment =get_or_generate_comment(post)

                post_comment(post["id"], comment)

                print("\n==============================")
                print("TRENDING POST FOUND")
                print("==============================")

                print("Score:", score)
                print("ID:", post["id"])
                print("Time:", post["date"])
                print("Likes:", post["likes"])
                print("Comments:", post["comments"])
                print("Reposts:", post["reposts"])

                print("\nText:\n", post["text"])
                print("\nComment:", comment)

            index += 1

            # scroll every 3 posts
            if index % 3 == 0:
                scroll_feed()

        print("\nCycle finished. Returning to top...\n")

        scroll_top()

        time.sleep(
            random.uniform(SCAN_DELAY_MIN, SCAN_DELAY_MAX)
        )


if __name__ == "__main__":
    run_agent()
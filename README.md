# LinkedIn Trending Comment Bot (OpenClaw)

This project automates discovering trending LinkedIn posts and posting AI-generated comments using the OpenClaw browser.
The bot opens LinkedIn in a real Chrome session, scans posts from the feed, identifies trending ones based on engagement metrics, generates a relevant comment, and posts it automatically.

---

## Pipeline Overview

The system works in the following steps:

1. **Launch Browser**

   * Start the OpenClaw browser.
   * Open the LinkedIn feed in Chrome.

2. **Feed Loading**

   * Wait until the LinkedIn feed loads.
   * Scroll the page until enough posts are available for analysis.

3. **Post Extraction**

   * Extract post information using browser JavaScript:

     * Post ID (`data-urn`)
     * Post text
     * Time posted
     * Number of likes
     * Number of comments
     * Number of reposts

4. **Trending Post Detection**

   * Each post receives a score based on engagement.
   * Posts above a configurable threshold are considered **trending**.

5. **Comment Generation**

   * A comment is generated for the trending post using an AI model.

6. **Automated Comment Posting**

   * The bot locates the correct LinkedIn post.
   * Opens the comment box.
   * Inserts the generated comment.
   * Clicks the **Comment** button to submit the comment.

---

## Technologies Used

* Python
* OpenClaw Browser Automation
* JavaScript DOM Execution
* LinkedIn Web Interface

---

## Key Features

* Automated LinkedIn feed scanning
* Trending post detection
* AI-generated contextual comments
* Real browser automation via OpenClaw
* Works directly with LinkedIn UI (no API required)

---

## Project Structure

```
linkedin-openclaw-bot/

extract_posts.py       # LinkedIn feed extraction
comment_poster.py      # Comment posting automation
config.py              # Configuration variables
main.py       # Full automation pipeline
README.md
```

---

## Requirements

* Python 3.9+
* OpenClaw CLI installed
* LinkedIn account

---

## Running the Bot

1. Start OpenClaw browser.
2. Login to LinkedIn when prompted.
3. Run the pipeline

---

## Notes

* The bot uses the LinkedIn web interface, not official APIs.
* Random delays should be added to avoid LinkedIn rate limits.
* Manual login may be required when the browser starts.



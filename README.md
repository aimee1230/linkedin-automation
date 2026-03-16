# LinkedIn AI Comment Automation Bot (OpenClaw)

This project implements an **AI-powered LinkedIn automation bot** that discovers relevant LinkedIn posts and automatically posts contextual comments.

The bot uses **OpenClaw browser automation** to control a real Chrome session, extract profile information, generate topic keywords, search LinkedIn posts, detect trending posts based on engagement, and generate AI comments.

This system demonstrates how **LLM-powered agents can automate social media interactions using real browser environments**.

---

# Pipeline Overview

The bot operates in the following sequence.

---

## 1. Launch Browser

Start the **OpenClaw browser automation environment**.

The bot opens LinkedIn in a **real Chrome session**.

The user logs in manually if required.

---

## 2. Profile Analysis

The bot analyzes the user's LinkedIn profile to understand their professional interests.

### Steps

1. Open the user profile page
2. Scroll until the **About section** becomes visible
3. Extract profile content including:

* About section text
* Headline (optional)

This information is used to determine **relevant topics for engagement**.

---

## 3. Keyword Generation

An AI model analyzes the extracted profile content and generates **content topics relevant to the user**.

### Example Output

```python
[
 "project management",
 "agile methodology",
 "team leadership",
 "workflow optimization",
 "business productivity"
]
```

These keywords are used to search LinkedIn posts.

---

## 4. LinkedIn Post Search

For each generated keyword, the bot navigates to the LinkedIn search page:

```
https://www.linkedin.com/search/results/content/?keywords=<keyword>
```

Posts related to that topic are loaded dynamically.

---

## 5. Post Extraction

Visible posts are extracted directly from the LinkedIn page using **JavaScript DOM evaluation via OpenClaw**.

The bot collects the following information:

* Post ID
* Post text
* Time posted
* Number of likes
* Number of comments
* Number of reposts

Posts without sufficient content are ignored.

---

## 6. Trending Post Detection

Each post receives an **engagement score** using the following formula:

```
engagement_score = likes + (2 × comments) + (3 × reposts)
```

Posts above a configurable threshold are considered **trending posts**.

---

## 7. AI Comment Generation

For trending posts, an **AI model generates a contextual LinkedIn comment**.

The prompt instructs the model to:

* Sound natural and human
* Add a small insight
* Keep the comment short
* Avoid promotional language

### Example Generated Comment

```
Interesting perspective. Strong project coordination is often the key factor
that determines whether timelines succeed or slip. How do you usually handle
cross-team dependencies in large projects?
```

---

## 8. Automated Comment Posting

The bot posts the generated comment directly on LinkedIn.

### Steps

1. Locate the correct post using its **data-urn**
2. Click the **Comment button**
3. Focus the comment editor
4. Simulate natural typing
5. Submit the comment

---

## 9. Continuous Operation

The bot continuously cycles through keywords and scans new posts.

### Workflow Loop

```
search keyword → scan posts → detect trending → comment → next keyword
```

This allows the system to continuously **discover and interact with new posts**.

---

## Technologies Used

* Python
* OpenClaw Browser Automation
* JavaScript DOM Execution
* Ollama / Qwen LLM
* LinkedIn Web Interface

The system interacts directly with **LinkedIn's web interface instead of using APIs**.

---

## Key Features

* Real Chrome browser automation via OpenClaw
* LinkedIn profile analysis
* AI-generated topic discovery
* Automated LinkedIn post search
* Trending post detection
* AI-generated contextual comments
* Automated comment posting
* Duplicate comment prevention using memory storage

---

## Project Structure

```
linkedin-openclaw-bot/

linkedin_bot.py              # Main automation pipeline

linkedin_feed_reader.py      # Extract LinkedIn posts
trending_detector.py         # Engagement scoring logic

comment_generator.py         # AI comment generation
linkedin_comment_bot.py      # Comment posting automation

profile_reader.py            # LinkedIn profile extraction
topic_generator.py           # Keyword generation from profile
linkedin_search.py           # LinkedIn keyword search

keyword_memory.py            # Keyword storage
config.py                    # Configuration parameters
prompts.py                   # LLM prompts

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



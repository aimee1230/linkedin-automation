import subprocess
import time
import json
import random

from config import POSTS_TO_SCAN, TRENDING_THRESHOLD, SCAN_DELAY_MIN, SCAN_DELAY_MAX

# Run shell command
def run_cmd(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

# Start OpenClaw browser
def start_browser():
    print("Starting OpenClaw browser...")
    run_cmd("openclaw browser start")
    time.sleep(5)

# Open LinkedIn Feed
def open_linkedin():
    print("Opening LinkedIn feed...")
    run_cmd(
        "openclaw browser open https://www.linkedin.com/feed/"
    )
    print("Login manually if required...")
    time.sleep(25)


# Wait until feed loads
def wait_for_feed():
    print("Waiting for LinkedIn feed to load...")
    js = """
() => {
return document.querySelectorAll("div.feed-shared-update-v2").length;
}
"""
    while True:
        output = run_cmd(
            f"openclaw browser evaluate --fn '{js}'"
        )
        try:
            count = int(output)
        except:
            count = 0
        if count > 0:
            print("Feed loaded.")
            break
        print("Feed not ready yet...")
        time.sleep(3)

# Scroll until required posts loaded
def load_posts():

    js = """
() => {
return document.querySelectorAll("div.feed-shared-update-v2").length;
}
"""

    while True:
        output = run_cmd(
            f"openclaw browser evaluate --fn '{js}'"
        )
        try:
            count = int(output)
        except:
            count = 0
        print("Posts currently loaded:", count)
        if count >= POSTS_TO_SCAN:
            break
        run_cmd(
            'openclaw browser evaluate --fn "() => window.scrollBy(0,2000)"'
        )
        time.sleep(2)

# Extract posts
def scan_feed(index):

    js = f"""
() => {{

/* -----------------------------
GET POSTS
----------------------------- */

const containers = Array.from(
 document.querySelectorAll("div.feed-shared-update-v2")
);

if(containers.length <= {index}){{
 return null;
}}

const post = containers[{index}];


/* -----------------------------
EXPAND SEE MORE
----------------------------- */

post.querySelectorAll("button").forEach(btn => {{

 if(btn.innerText.toLowerCase().includes("see more")){{
  btn.click();
 }}

}});


/* -----------------------------
INITIALIZE VARIABLES
----------------------------- */

let text = "";
let date = "";
let likes = 0;
let comments = 0;
let reposts = 0;
let id = "";


/* -----------------------------
POST ID
----------------------------- */

id = post.getAttribute("data-urn") || "";


/* -----------------------------
POST TEXT
----------------------------- */

const textBlock = post.querySelector("span.break-words");

if(textBlock){{

 text = textBlock.innerText
       .replace(/hashtag\\s*/gi,"")
       .replace(/Follow/gi,"")
       .trim();

}}


/* -----------------------------
POST TIME
----------------------------- */

const timeBlock = post.querySelector(
"span.update-components-actor__sub-description"
);

if(timeBlock){{

 const raw = timeBlock.innerText;

 const match = raw.match(/[0-9]+[smhdw]/);

 if(match){{
  date = match[0];
 }}

}}


/* -----------------------------
SOCIAL COUNTS
----------------------------- */

const social = post.querySelector(
".social-details-social-counts"
);

if(social){{

 const raw = social.innerText;

 const likeMatch =
  raw.match(/([0-9,]+)\\s*(reactions|likes)/i) ||
  raw.match(/👍\\s*([0-9,]+)/) ||
  raw.match(/^([0-9,]+)/);

 const commentMatch =
  raw.match(/([0-9,]+)\\s*comments?/i);

 const repostMatch =
  raw.match(/([0-9,]+)\\s*reposts?/i);

 if(likeMatch){{
  likes = likeMatch[1].replace(/,/g,"");
 }}

 if(commentMatch){{
  comments = commentMatch[1].replace(/,/g,"");
 }}

 if(repostMatch){{
  reposts = repostMatch[1].replace(/,/g,"");
 }}

}}


/* -----------------------------
FILTER EMPTY POSTS
----------------------------- */

if(text.length < 40){{
 return null;
}}


/* -----------------------------
RETURN POST
----------------------------- */

return {{

 id:id,
 text:text,
 date:date,
 likes:likes,
 comments:comments,
 reposts:reposts

}};

}}
"""

    output = run_cmd(
        f"openclaw browser evaluate --fn '{js}'"
    )

    try:
        return json.loads(output)

    except:

        print("Raw output:", output)

        return None

# -----------------------------------
# Scroll back to top
# -----------------------------------
def scroll_top():

    run_cmd(
        'openclaw browser evaluate --fn "() => window.scrollTo(0,0)"'
    )

def scroll_feed():

    print("Scrolling feed...")

    run_cmd(
        'openclaw browser evaluate --fn "() => window.scrollBy(0,1500)"'
    )

    time.sleep(2)
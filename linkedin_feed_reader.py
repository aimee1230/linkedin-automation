import subprocess
import time
import json


# -----------------------------------
# Run shell command
# -----------------------------------

def run_cmd(cmd):

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


# -----------------------------------
# Start OpenClaw browser
# -----------------------------------

def start_browser():

    print("Starting OpenClaw browser...")

    run_cmd("openclaw browser start")

    time.sleep(5)


# -----------------------------------
# Open LinkedIn for login
# -----------------------------------

def open_linkedin():

    print("Opening LinkedIn...")

    run_cmd(
        "openclaw browser open https://www.linkedin.com/feed/"
    )

    print("Login manually if required...")

    time.sleep(3)


# -----------------------------------
# Wait until posts appear
# -----------------------------------

def wait_for_posts(timeout=30):

    print("Waiting for posts to load...")

    js = """
() => {
return document.querySelectorAll("div.feed-shared-update-v2").length;
}
"""

    start_time = time.time()

    while True:

        output = run_cmd(
            f"openclaw browser evaluate --fn '{js}'"
        )

        try:
            count = int(output)
        except:
            count = 0

        if count > 0:
            print("Posts detected.")
            return True

        if time.time() - start_time > timeout:
            print("Timeout waiting for posts.")
            return False

        time.sleep(2)


# -----------------------------------
# Extract all visible posts
# -----------------------------------

def scan_visible_posts():

    js = """
() => {

const containers = Array.from(
 document.querySelectorAll("div.feed-shared-update-v2")
);

const results = [];

containers.forEach(post => {

 let id = post.getAttribute("data-urn") || "";

 if(!id) return;

 let text = "";
 let date = "";
 let likes = 0;
 let comments = 0;
 let reposts = 0;


/* -----------------------------
POST TEXT
----------------------------- */

 const textBlock = post.querySelector("span.break-words");

 if(textBlock){

  text = textBlock.innerText
         .replace(/hashtag\\s*/gi,"")
         .replace(/Follow/gi,"")
         .trim();

 }

 if(text.length < 40) return;


/* -----------------------------
POST TIME
----------------------------- */

 const timeBlock = post.querySelector(
 "span.update-components-actor__sub-description"
 );

 if(timeBlock){

  const raw = timeBlock.innerText;

  const match = raw.match(/[0-9]+[smhdw]/);

  if(match){
   date = match[0];
  }

 }


/* -----------------------------
SOCIAL COUNTS
----------------------------- */

 const social = post.querySelector(
 ".social-details-social-counts"
 );

 if(social){

  const raw = social.innerText;

  const likeMatch =
   raw.match(/([0-9,]+)\\s*(reactions|likes)/i) ||
   raw.match(/👍\\s*([0-9,]+)/) ||
   raw.match(/^([0-9,]+)/);

  const commentMatch =
   raw.match(/([0-9,]+)\\s*comments?/i);

  const repostMatch =
   raw.match(/([0-9,]+)\\s*reposts?/i);

  if(likeMatch){
   likes = likeMatch[1].replace(/,/g,"");
  }

  if(commentMatch){
   comments = commentMatch[1].replace(/,/g,"");
  }

  if(repostMatch){
   reposts = repostMatch[1].replace(/,/g,"");
  }

 }

 results.push({

  id:id,
  text:text,
  date:date,
  likes:likes,
  comments:comments,
  reposts:reposts

 });

});

return results;

}
"""

    output = run_cmd(
        f"openclaw browser evaluate --fn '{js}'"
    )

    try:
        return json.loads(output)

    except:
        return []


# -----------------------------------
# Scroll feed
# -----------------------------------

def scroll_feed():

    print("Scrolling feed...")

    run_cmd(
        'openclaw browser evaluate --fn "() => window.scrollBy(0,1500)"'
    )

    time.sleep(2)


# -----------------------------------
# Scroll to top
# -----------------------------------

def scroll_top():

    run_cmd(
        'openclaw browser evaluate --fn "() => window.scrollTo(0,0)"'
    )
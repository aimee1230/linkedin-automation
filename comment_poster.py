import subprocess
import time


def run_cmd(cmd):

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.stderr:
        print("ERROR:", result.stderr)

    return result.stdout.strip()


def post_comment(post_id, comment_text):

    print("\nPosting comment on:", post_id)

    js = f"""
() => {{

const postId = "{post_id}";
const commentText = `{comment_text}`;


// -----------------------------
 // Find the post
 // -----------------------------

const posts = document.querySelectorAll("div[data-urn]");

let targetPost = null;

for (const post of posts) {{

    if (post.getAttribute("data-urn") === postId) {{
        targetPost = post;
        break;
    }}

}}

if (!targetPost) return "post_not_found";


// -----------------------------
 // Scroll to post
 // -----------------------------

targetPost.scrollIntoView({{block:"center"}});


// -----------------------------
 // Click comment icon
 // -----------------------------

const commentBtn =
    targetPost.querySelector('button[aria-label*="Comment"]') ||
    targetPost.querySelector('button[data-control-name="comment"]');

if (!commentBtn) return "comment_icon_not_found";

commentBtn.click();


// -----------------------------
 // Wait for editor
 // -----------------------------

setTimeout(() => {{

    const editor = document.querySelector('[contenteditable="true"]');

    if (!editor) return;

    editor.focus();

    editor.innerText = commentText;

    editor.dispatchEvent(
        new InputEvent("input", {{bubbles:true}})
    );


    // -----------------------------
    // Click submit button
    // -----------------------------

    setTimeout(() => {{

        const buttons = document.querySelectorAll("button");

        for (const btn of buttons) {{

            if (btn.innerText.trim() === "Comment") {{

                btn.click();
                break;

            }}

        }}

    }}, 700);

}}, 1200);


return "comment_process_started";

}}
"""

    run_cmd([
        "openclaw",
        "browser",
        "evaluate",
        "--fn",
        js
    ])

    time.sleep(4)

    print("Comment posted")
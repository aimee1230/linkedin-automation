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

    if not comment_text:
        print("No comment provided")
        return


    js_comment = f"""
() => {{

const post = document.querySelector(`div[data-urn="{post_id}"]`);
if (!post) return "post_not_found";

post.scrollIntoView({{behavior:"smooth", block:"center"}});


// STEP 1 — click comment icon
const commentBtn =
    post.querySelector('button[aria-label*="Comment"]') ||
    post.querySelector('button[data-control-name="comment"]');

if (!commentBtn) return "comment_button_not_found";

commentBtn.click();


// STEP 2 — wait for editor
setTimeout(() => {{

    const editor = post.querySelector('div[contenteditable="true"]');

    if (!editor) {{
        console.log("editor_not_found");
        return;
    }}

    editor.focus();

    const text = `{comment_text}`;

    // Clear editor
    editor.innerHTML = "";

    // STEP 3 — simulate real typing
    for (let i = 0; i < text.length; i++) {{

        const char = text[i];

        editor.innerHTML += char;

        editor.dispatchEvent(new KeyboardEvent("keydown", {{
            bubbles: true,
            key: char
        }}));

        editor.dispatchEvent(new InputEvent("input", {{
            bubbles: true,
            inputType: "insertText",
            data: char
        }}));

        editor.dispatchEvent(new KeyboardEvent("keyup", {{
            bubbles: true,
            key: char
        }}));
    }}


    // STEP 4 — wait and click comment button
    setTimeout(() => {{

        const submitBtn =
            post.querySelector('button.artdeco-button--primary') ||
            post.querySelector('button[type="submit"]');

        if (!submitBtn) {{
            console.log("submit_button_not_found");
            return;
        }}

        submitBtn.disabled = false;

        submitBtn.click();

        console.log("comment_posted");

    }}, 1500);


}}, 1500);

return "processing";

}}
"""


    result = run_cmd([
        "openclaw",
        "browser",
        "evaluate",
        "--fn",
        js_comment
    ])

    print("OpenClaw result:", result)

    time.sleep(6)

    print("Comment process finished")
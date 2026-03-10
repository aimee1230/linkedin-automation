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


    // STEP 3 — simulate real typing
    editor.textContent = "";
    
    const text = `{comment_text}`;
    
    for (let i = 0; i < text.length; i++) {{
        editor.textContent += text[i];

        editor.dispatchEvent(new InputEvent("input", {{
            bubbles: true,
            inputType: "insertText",
            data: text[i]
        }}));
    }}


    // STEP 4 — find correct comment form
    setTimeout(() => {{

        const form = post.querySelector("form");
        if (!form) {{
            console.log("comment_form_not_found");
            return;
        }}

        const submit = form.querySelector("button[type='submit']");
        if (!submit) {{
            console.log("submit_button_not_found");
            return;
        }}

        submit.click();

        console.log("comment_posted");

    }}, 1200);


}}, 1200);


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

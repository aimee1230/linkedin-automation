import subprocess
import time
import json


def run_cmd(cmd):

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.stderr:
        print("ERROR:", result.stderr)

    return result.stdout.strip()


def get_snapshot():

    return run_cmd([
        "openclaw",
        "browser",
        "snapshot",
        "--json"
    ])


def get_editor_ref(snapshot):

    data = json.loads(snapshot)
    refs = data.get("refs", {})

    for ref, node in refs.items():
        if node.get("role") == "textbox":
            return ref

    return None


def get_submit_ref(snapshot):

    data = json.loads(snapshot)
    refs = data.get("refs", {})

    for ref, node in refs.items():

        role = node.get("role", "")
        name = node.get("name", "").lower()

        if role == "button" and name.strip() == "comment":
            return ref

    return None


def post_comment(post_id, comment_text):

    print("\nPosting comment on:", post_id)

    if not comment_text:
        return


    # STEP 1 — open comment box
    js_open_comment = f"""
() => {{

const posts = document.querySelectorAll("div[data-urn]");

for (const post of posts) {{

    if (post.getAttribute("data-urn") === "{post_id}") {{

        const btn =
            post.querySelector('button[aria-label*="Comment"]') ||
            post.querySelector('button[data-control-name="comment"]');

        if (!btn) return "comment_button_not_found";

        post.scrollIntoView({{behavior:"smooth", block:"center"}});
        btn.click();

        return "comment_box_opened";
    }}
}}

return "post_not_found";

}}
"""

    run_cmd([
        "openclaw",
        "browser",
        "evaluate",
        "--fn",
        js_open_comment
    ])

    time.sleep(3)


    # STEP 2 — find editor
    snapshot = get_snapshot()

    editor_ref = get_editor_ref(snapshot)

    if not editor_ref:
        print("Editor not found")
        return


    # STEP 3 — type comment
    run_cmd([
        "openclaw",
        "browser",
        "type",
        editor_ref,
        comment_text
    ])

    time.sleep(1)


    # 🔥 NEW FIX — activate LinkedIn editor
    run_cmd([
        "openclaw",
        "browser",
        "press",
        "Enter"
    ])

    time.sleep(1)


    # STEP 4 — find submit button
    snapshot = get_snapshot()

    submit_ref = get_submit_ref(snapshot)

    if not submit_ref:
        print("Submit button not found")
        return


    # STEP 5 — click comment button
    run_cmd([
        "openclaw",
        "browser",
        "click",
        submit_ref
    ])

    print("Comment posted successfully")

    time.sleep(3)

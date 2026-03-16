import subprocess
import time
import json


def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def open_profile():

    print("Opening LinkedIn profile...")

    run_cmd(
        'openclaw browser evaluate --fn "() => window.location.href=\'https://www.linkedin.com/in/me/\'"'
    )

    time.sleep(8)


def about_visible():

    js = """
() => {

const headings = Array.from(document.querySelectorAll("h2"));

return headings.some(h => h.innerText.trim() === "About");

}
"""

    output = run_cmd(
        f"openclaw browser evaluate --fn '{js}'"
    )

    return "true" in output.lower()

def extract_about():

    js = """
() => {

const section = Array.from(document.querySelectorAll("section"))
.find(sec => sec.querySelector("h2")?.innerText.trim() === "About");

if(!section) return null;

/* expand see more */

const btn = Array.from(section.querySelectorAll("button"))
.find(b => b.innerText.toLowerCase().includes("more"));

if(btn) btn.click();

let about = "";

section.querySelectorAll("span").forEach(span => {

 const txt = span.innerText.trim();

 if(txt.length > about.length){
  about = txt;
 }

});

return about;

}
"""

    output = run_cmd(
        f"openclaw browser evaluate --fn '{js}'"
    )

    if output and output != "null":
        return output.strip('"')

    return None

def scroll_page():

    run_cmd(
        'openclaw browser evaluate --fn "() => { \
            const main=document.querySelector(\'main\'); \
            if(main){ main.scrollBy(0,500); } \
        }"'
    )


def extract_profile_data():
    open_profile()
    print("Searching for About section...")
    about = None
    for _ in range(5):
        if about_visible():
            print("About section detected.")
            time.sleep(2)
            about = extract_about()
            break
        scroll_page()
        print("Scrolling profile...")
        time.sleep(3)
    if not about:
        print("About section not found.")
        return None
    profile = {
        "about": about
    }
    return profile
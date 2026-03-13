import subprocess
import json
import time


# -----------------------------
# Run shell command
# -----------------------------
def run_cmd(cmd):

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


# -----------------------------
# Open profile page
# -----------------------------
def open_profile():

    print("Opening profile page...")

    run_cmd(
        'openclaw browser evaluate --fn "() => window.location.href=\'https://www.linkedin.com/in/me/\'"'
    )

    time.sleep(8)


# -----------------------------
# Wait until profile loads
# -----------------------------
def wait_for_profile(timeout=30):

    print("Waiting for profile to load...")

    js = """
() => {
return document.querySelector("main") !== null;
}
"""

    start = time.time()

    while True:

        output = run_cmd(
            f"openclaw browser evaluate --fn '{js}'"
        )

        if "true" in output.lower():
            print("Profile page loaded.")
            return True

        if time.time() - start > timeout:
            print("Profile load timeout.")
            return False

        time.sleep(2)


# -----------------------------
# Extract profile data
# -----------------------------
def extract_profile_data():

    wait_for_profile()

    js = """
() => {

let headline = "";
let about = "";


/* ---------------------------------
EXPAND ABOUT (CLICK SEE MORE)
--------------------------------- */

const aboutSection = Array.from(document.querySelectorAll("section"))
.find(s => s.innerText.includes("About"));

if(aboutSection){

 const btn = Array.from(aboutSection.querySelectorAll("button"))
 .find(b => b.innerText.toLowerCase().includes("more"));

 if(btn){
  btn.click();
 }

}


/* ---------------------------------
HEADLINE
--------------------------------- */

const headlineNode =
document.querySelector(".text-body-medium.break-words") ||
document.querySelector(".text-body-medium");

if(headlineNode){
 headline = headlineNode.innerText.trim();
}


/* ---------------------------------
ABOUT TEXT
--------------------------------- */

if(aboutSection){

 const spans = aboutSection.querySelectorAll("span");

 spans.forEach(span => {

  const txt = span.innerText.trim();

  if(txt.length > about.length){
   about = txt;
  }

 });

}


return {
 headline: headline,
 about: about
};

}
"""

    output = run_cmd(
        f"openclaw browser evaluate --fn '{js}'"
    )

    try:

        data = json.loads(output)

        print("\nProfile Headline:", data.get("headline", ""))
        print("Profile About:", data.get("about", ""))

        return data

    except:

        print("Profile extraction failed")
        print(output)

        return None
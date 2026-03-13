import subprocess
import time


def open_keyword_search(keyword):

    keyword_url = keyword.replace(" ", "%20")

    url = f"https://www.linkedin.com/search/results/content/?keywords={keyword_url}"

    subprocess.run(
        f'openclaw browser evaluate --fn "() => window.location.href=\'{url}\'"',
        shell=True
    )

    print(f"\nSearching posts for keyword: {keyword}")

    time.sleep(5)
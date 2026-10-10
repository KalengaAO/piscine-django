import requests 
import sys
from bs4 import BeautifulSoup

def get_first_link(url):
    try:
        headers = { "User-Agent": "Mozilla/5.0" }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1", id="firstHeading").text.strip()

        for content in soup.find_all("div", class_="mw-parser-output"):
            parenthisis_count = 0
            for p in content.find_all("p", recursive=False):
                for elem in p.descendants:
                    text = str(elem)
                    if "(" in text:
                        parenthisis_count += text.count('(')
                    if ")" in text:
                        parenthisis_count -= text.count(')')
                    if elem.name == "a":
                        href = elem.get("href")
                        if (href
                            and href.startswith("/wiki/")
                            and not href.startswith("/wiki/help:")
                            and parenthisis_count == 0
                            and not elem.find_parent(["i", "em"])
                            ):
                            return  f"https://en.wikipedia.org/wiki/{href}", title
        return None, title
    except Exception:
        return None, None

def roads_to_philosophy(string_to_search: str) -> None:
    base_url = "https://en.wikipedia.org/wiki/"
    visited = []
    current_url = base_url + string_to_search.replace(" ", "_")
    while True:
        if current_url in visited:
            print("It leads to an Infinie loop!")
            break

        next_url, title = get_first_link(current_url)
        if not title:
            print(f"{title} It is a dead end!!")
            break
        visited.append(title)

        if title == "Philosophy":
            print(f"{len(visited)} roads from {visited[0]} to Phylosophy !")
            break

        if not next_url:
            print("It is a dead end!!")
            break
        current_url = next_url

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} [string_to_search]")
        sys.exit(1)

    string_to_search = sys.argv[1]
    if not string_to_search:
        print("string_to_search can't be empty!")
        sys.exit(1)

    roads_to_philosophy(string_to_search)
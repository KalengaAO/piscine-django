import json
import sys
import dewiki
import requests

def request(search_term: str):
    url = "https://pt.wikipedia.org/w/api.php"
    headers = {"User-Agent" : "Mozilla/5.0"}
    params = {
        "action": "query",
        "prop" : "extracts",
        "explaintext": True,
        "titles" : search_term,
        "format" :  "json",
        "redirects" : 1,
        "srinfo" : "suggestion",
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            print(f"No result found fo '{search_term}'")
            return
        
        for page_id, page in pages.items():
            if page_id == -1 or page.get("extract") is None:
                print(f"No result found for '{search_term}")
                return
            raw_extrat = page.get("extract").strip()
            if not raw_extrat:
                print(f"No result found for '{search_term}'")
                return
            extract = dewiki.from_string(raw_extrat)

            with    open(f"{search_term}.wiki", "w", encoding="utf-8") as file:
                file.write(extract)

    except requests.exceptions.RequestException as e:
        print("An error occured during request:", e)
    except json.JSONDecodeError:
        print("Filed to parser the response from the server")
    except Exception as e:
        print("Unexpected error: ", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [string-to-search]")
        sys.exit(1)

    search_term = sys.argv[1].strip()
    if not search_term:
        print("Search term can't be empty!")
        sys.exit(1)

    request(search_term)
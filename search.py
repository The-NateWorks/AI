import requests, bs4, re
from urllib.parse import quote


def extract_search_query(text):
    text = text.lower()
    for prefix in ["search ", "look up ", "find ", "who is "]:
        if text.startswith(prefix):
            return text[len(prefix):]
    return text

def search_query(query):
    res = requests.get(
        "https://api.duckduckgo.com/",
        params= {
            "q": query,
            "format": "json",
            "no_html": 1
        }
    )
    return res.json()

def fetch_url(url):
    res = requests.get(url, timeout=10, headers = {"User-Agent": "NateSearchBot/1.0 (Educational project; contact: https://example.com)"})
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    content = soup.select_one(".mw-parser-output")
    if not content:
        return []

    paragraphs = []
    for p in content.find_all("p"):
        text = p.get_text().strip()
        if len(text) > 0 and text.endswith(tuple(".!?")):  # skip junk
            paragraphs.append(text)

    return paragraphs[:5]

def summarize(text, max_sentences=5):
    # Clean up whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split into sentences using punctuation
    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Filter out very short or title-like sentences
    sentences = [s for s in sentences if len(s.split()) > 4]

    for i,s in enumerate(sentences):
        if s.endswith((".", "!", "?")):
            sentences[i] = s
        else:
            sentences[i] = s + "."

    if not sentences:
        summary = text
    else:
        summary = " ".join(sentences[:max_sentences])

    # Take the first few meaningful sentences
    return summary

def get_capital_words(text):
    capital = 0
    for word in text.split():
        if word[0].isupper() or word[0] in list("~`!@#$%^&*()_+-={}[]:\";''|\\/?.>,<"):
            capital += 1
    return capital, len(text.split())

def search(text):
    data = search_query(text)
    retdata = []
    if data["AbstractURL"]:
        topic = data["AbstractURL"].split("/")[-1]
        topic = quote(topic)
        url = f"https://en.wikipedia.org/wiki/{topic}"
        fetched = fetch_url(url)
        summary = summarize(" ".join(fetched))
        if summary:
            return summary
    if data["RelatedTopics"]:
        topics = data["RelatedTopics"]
        for t in topics:
            if "FirstURL" in t:
                topic = t["FirstURL"].split("/")[-1]
                topic = quote(topic)
                summary = summarize(" ".join(fetch_url(f"https://en.wikipedia.org/wiki/{topic}")))
                if summary:
                    retdata.append(summary)
    genSum = summarize(" ".join(retdata))
    if genSum.strip():
        return genSum
    else:
        return f"I couldn't find anything on \"{text}\""

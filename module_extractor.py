import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_all_links(url, domain):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        links = set()
        for a in soup.find_all('a', href=True):
            href = urljoin(url, a['href'])
            if domain in href:
                links.add(href.split('#')[0])
        return links
    except:
        return set()

def extract_html(url):
    try:
        return requests.get(url, timeout=10).text
    except:
        return ""

def parse_modules_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    modules = []
    current = None

    for tag in soup.find_all(['h1','h2','h3','h4','div']):
        text = tag.get_text(strip=True)
        if not text:
            continue

        # Module indicators: big headings or specific divs
        if tag.name in ['h1','h2'] or 'title' in tag.get('class',[]) or 'article-heading' in tag.get('class',[]):
            if current:
                modules.append(current)
            current = {'module': text, 'Description': '', 'Submodules': {}}

        # Submodule indicators: slightly smaller headings
        elif tag.name in ['h3','h4']:
            if current:
                current['Submodules'][text] = ''

        # Paragraphs or div blocks
        elif tag.name in ['div','p'] and current:
            # assign to latest submodule if exists, else module
            subkeys = list(current['Submodules'].keys())
            if subkeys:
                current['Submodules'][subkeys[-1]] += ' ' + text
            else:
                current['Description'] += ' ' + text

    if current:
        modules.append(current)
    return modules

def crawl_and_parse(url):
    if not is_valid_url(url):
        return {}

    domain = urlparse(url).netloc
    visited = set()
    to_visit = {url}
    output = {}

    while to_visit and len(visited) < 5:
        page = to_visit.pop()
        if page in visited:
            continue
        visited.add(page)
        html = extract_html(page)
        modules = parse_modules_from_html(html)
        output[page] = modules
        to_visit.update(get_all_links(page, domain) - visited)

    return output

if __name__ == "__main__":
    start = input("Enter documentation URL: ")
    result = crawl_and_parse(start)
    with open("output_preview.json","w") as f:
        json.dump(result, f, indent=2)
    print("Done — check output_preview.json")

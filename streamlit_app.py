import streamlit as st
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
        for a_tag in soup.find_all('a', href=True):
            href = urljoin(url, a_tag['href'])
            if domain in href:
                links.add(href.split('#')[0])
        return links
    except:
        return set()

def extract_content(url):
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except:
        return ""

def parse_modules_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    modules = []
    current_module = None

    for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
        if tag.name == 'h1':
            if current_module:
                modules.append(current_module)
            current_module = {
                'module': tag.get_text(strip=True),
                'Description': '',
                'Submodules': {}
            }
        elif tag.name == 'h2' and current_module:
            current_sub = tag.get_text(strip=True)
            current_module['Submodules'][current_sub] = ''
        elif tag.name == 'p' and current_module:
            last_key = list(current_module['Submodules'].keys())[-1] if current_module['Submodules'] else None
            if last_key:
                current_module['Submodules'][last_key] += ' ' + tag.get_text(strip=True)
            else:
                current_module['Description'] += ' ' + tag.get_text(strip=True)

    if current_module:
        modules.append(current_module)

    return modules

def crawl_and_parse(url):
    if not is_valid_url(url):
        return {}

    domain = urlparse(url).netloc
    visited = set()
    to_visit = set([url])
    output = {}

    while to_visit and len(visited) < 5:
        current_url = to_visit.pop()
        if current_url in visited:
            continue

        visited.add(current_url)
        html = extract_content(current_url)
        modules = parse_modules_from_html(html)
        output[current_url] = modules
        links = get_all_links(current_url, domain)
        to_visit.update(links - visited)

    return output

st.title("📚 Pulse Module Extractor")
st.markdown("Extract structured modules and submodules from help documentation URLs.")

url_input = st.text_input("Enter a documentation URL:")

if st.button("Extract Modules") and url_input:
    with st.spinner("Crawling and extracting..."):
        result = crawl_and_parse(url_input)
    st.success("Extraction complete!")
    st.json(result)

    # Optional: Download output
    st.download_button(
        label="Download JSON",
        data=json.dumps(result, indent=2),
        file_name="extracted_modules.json",
        mime="application/json"
    )

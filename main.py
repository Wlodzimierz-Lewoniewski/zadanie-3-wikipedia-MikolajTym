import re
from urllib.parse import quote

import requests

category = input().strip()
category = category.replace(" ", "_")
category = quote(category)

category = f"/Kategoria:{category}" # convert to encoded HTML
wiki_url = "https://pl.wikipedia.org/wiki"
response = requests.get(wiki_url+category).text

p = re.compile(r'<a.+href="\/wiki([^:]+?)".+?>(.+)<\/a>')
links = re.findall(p, response)[1:3]

for link in links:
    p = re.compile(r'<li>.*?</li>')
    links = re.findall(p, response)[:2]
    links = [re.findall(re.compile(r'href="(.*?)".*?>(.*?)<\/a>'), link) for link in links]

    response_1 = requests.get(wiki_url+link[0]).text
    start = re.search(re.compile(r'id="mw-content-text"'), response_1).start()
    text = response_1[start:]
    links = re.findall(re.compile(r'href="[^:]+?".+?title="(.*?)"'), text)[:5]
    print(" | ".join(links))

    images = re.findall(re.compile(r'<img.+?src="(.+?)"'), text)[:3]
    print(" | ".join(images))

    start = re.search(re.compile(r'id="Przypisy"'), text).start()
    sources = text[start:]
    links = re.findall(re.compile(r'href="(http.+?)"'), sources)[:3]
    print(" | ".join(links))

    start = re.search(re.compile('id="catlinks"'), text).start()
    categories = text[start:]
    categories = re.findall(re.compile(r'<li.+?>(.+?)</a></li>'), categories)[:3]
    print(" | ".join(categories))
    
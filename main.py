import re
from urllib.parse import quote

import requests

category = input().strip()
category = category.replace(" ", "_")
category = quote(category)

category = f"/Kategoria:{category}"
wiki_url = "https://pl.wikipedia.org/wiki"
response = requests.get(wiki_url+category).text

main_content = response[re.search(re.compile(r'mw-category-generated'), response).start():]
p = re.compile(r'<a.+href="\/wiki([^:]+?)".+?>(.+)<\/a>')
links = re.findall(p, main_content)[:2]

for link in links:
    p = re.compile(r'<li>.*?</li>')
    links_p = re.findall(p, response)[:2]
    links_p = [re.findall(re.compile(r'href="(.*?)".*?>(.*?)<\/a>'), link) for link in links_p]

    response_1 = requests.get(wiki_url+link[0]).text
    start = re.search(re.compile(r'id="mw-content-text"'), response_1).start()
    text = response_1[start:]
    links_p = re.findall(re.compile(r'href="[^:]+?".+?title="(.*?)"'), text)[:5]
    print(" | ".join(links_p))

    images = re.findall(re.compile(r'<img.+?src="(.+?)"'), text)[:3]
    print(" | ".join(images))

    sources_text = re.search(re.compile(r'id="Przypisy"(.+)', re.DOTALL), text)
    if sources_text is not None:
        sources_text = re.search(re.compile(r'class="references"(.+?)<\/ol>', re.DOTALL), sources_text.group()).group()
        links_p = re.findall(re.compile(r'"(http.+?)"'), sources_text)
        if len(links_p) > 3:
            links_p = links_p[:3]
        print(" | ".join(links_p))

    categories_text = re.search(re.compile('mw-normal-catlinks(.+?)</div>'), text).group()
    categories = re.findall(re.compile(r'<li.+?>(.+?)</a></li>'), categories_text)
    if len(categories) > 3:
        categories = categories[:3]
    print(" | ".join(categories))
    
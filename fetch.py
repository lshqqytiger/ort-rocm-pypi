import os
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Tag


hostname = 'https://download.onnxruntime.ai/'
html = requests.get(hostname)
page = bs(html.text, 'html.parser').find('body')

package_indexes = {}
h3 = 0
for e in page:
    if not isinstance(e, Tag):
        continue
    if e.name == 'h3':
        h3 += 1
    elif e.name == 'a' and h3 in (1, 3,):
        text = e.get_text()
        if 'rocm' not in text:
            continue
        package_indexes[e.get_text().split('rocm')[1][:-5]] = e.attrs['href']

INDEX_HTML = '''<!DOCTYPE html>
<html>
    <head></head>
    <body>
        <a href="onnxruntime-training/">onnxruntime-training</a>
    </body>
</html>'''
for k, v in package_indexes.items():
    index_dir = os.path.join('static', k)
    os.mkdir(index_dir)
    with open(os.path.join(index_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(INDEX_HTML)
    package_dir = os.path.join(index_dir, 'onnxruntime-training')
    os.mkdir(package_dir)
    html = requests.get(hostname + v)
    page = bs(html.text, 'html.parser')
    for e in page.find_all('a'):
        e.attrs['href'] = hostname + e.attrs['href']
    with open(os.path.join(package_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(str(page))

import os
import subprocess

import requests
from bs4 import BeautifulSoup

from lib.DocumentParser import DocumentParser
from lib.KeyCreator import KeyCreator

CACHE = 'cache'


def fetch_images(images):
    for image in images:
        out_file = '../src/' + image['name']
        if os.path.isfile(out_file):
            continue
        src_name = '../src/' + image['src_name']
        url = f'https://cloud.google.com{image["src"]}'
        r = requests.get(url, allow_redirects=True)
        open(src_name, 'wb').write(r.content)
        subprocess.run(
            f'inkscape {src_name} --export-file={out_file} --export-ignore-filters --export-ps-level=3 --without-gui'.split())


def create_index(articles):
    file = f'../src/{articles["directory"]}index.tex'
    with open(file, 'w') as outimage:
        outimage.write('\\chapter{' + articles['title'] + '}\n')
        for article in articles['articles']:
            article_file = f'{articles["directory"]}' + article.split('/').pop() + '.tex'
            outimage.write('\\input{' + article_file + '}\n')


def parse(articles):
    for article in articles['articles']:
        r = requests.get(article, allow_redirects=True)
        html_doc = r.content
        key_creator = KeyCreator(article.split('/')[1])
        parser = DocumentParser(html_doc, key_creator)
        parser.parse()
        article_file = f'../src/{articles["directory"]}' + article.split('/').pop() + '.tex'
        with open(article_file, 'w') as outimage:
            outimage.write(
                ''.join(
                    parser.get_nodes()
                ).replace(
                    ' .', '.'
                ).encode(
                    'utf-8'
                ).decode(
                    'ascii', errors='replace'
                ).replace(
                    '�', '?'
                )
            )
        fetch_images(parser.get_images())
        create_index(articles)


def prepare():
    if not os.path.isdir(CACHE):
        os.mkdir(CACHE)


def main():
    prepare()
    base_url = 'https://cloud.google.com'
    volumes = [
        '/compute/docs/concepts',
        '/iam/docs/concepts',
        '/dlp/docs/concepts',
        '/vpc/docs/concepts',
        '/storage/docs/concepts',
        '/identity/docs/concepts',
        '/sql/docs/concepts',
    ]
    for chapter in volumes:
        key = chapter.split('/')[1]
        html_doc = download(base_url, chapter)
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.title.text.split('|')[1].strip().replace(' Documentation', '')
        article = soup.find('div', {'class': 'devsite-article-body'})
        cards = article.find_all('div', {'class': 'card'})
        print('\\chapter{' + title + '}')
        print(key)
        for card in cards:
            links = card.find_all('a')
            for link in links:
                print(base_url + link.attrs['href'])
        exit(1)


def download(base_url, chapter):
    cache_name = CACHE + '/' + chapter[1:].replace('/', '_')
    if os.path.isfile(cache_name) and os.path.getsize(cache_name) > 0:
        with open(cache_name, 'r') as inimage:
            return inimage.read()
    r = requests.get(base_url + chapter, allow_redirects=True)
    content = r.content.decode('utf-8', 'strict')
    with open(cache_name, 'w') as outimage:
        outimage.write(content)
    return content


main()

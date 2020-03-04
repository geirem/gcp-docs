import os
import subprocess

import requests
from bs4 import BeautifulSoup

from lib.DocumentParser import DocumentParser
from lib.KeyCreator import KeyCreator

CACHE = 'cache'
BASE_DIR = '../src'
BASE_URL = 'https://cloud.google.com'


def fetch_images(images):
    for image in images:
        out_file = '../src/' + image['name']
        if os.path.isfile(out_file):
            continue
        src_name = '../src/' + image['src_name']
        url = image['src'] if image['src'].startswith(BASE_URL) else f'{BASE_URL}{image["src"]}'
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 404:
            return
        open(src_name, 'wb').write(r.content)
        subprocess.run(
            f'inkscape {src_name} --export-file={out_file} --export-ignore-filters --export-ps-level=3 --without-gui'.split())


def create_index(topic, articles):
    file = f'{BASE_DIR}/{topic}.tex'
    with open(file, 'w') as outimage:
        outimage.write('\\chapter{' + articles['title'] + '}\n')
        for article in articles['articles']:
            article_file = f'{articles["directory"]}' + article.split('/').pop() + '.tex'
            outimage.write('\\input{' + article_file + '}\n')


def parse(chapter, article_url):
    html_doc = download(article_url)
    key_creator = KeyCreator(chapter)
    parser = DocumentParser(html_doc, key_creator)
    parser.parse()
    article_file = f'../src/{chapter}/' + chapter.replace('/', '_') + '.tex'
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


def download(document):
    cache_name = CACHE + '/' + document[1:].replace('/', '_')
    if os.path.isfile(cache_name) and os.path.getsize(cache_name) > 0:
        with open(cache_name, 'r') as inimage:
            return inimage.read()
    r = requests.get(BASE_URL + document, allow_redirects=True)
    content = r.content.decode('utf-8', 'strict')
    with open(cache_name, 'w') as outimage:
        outimage.write(content)
    return content


def prepare():
    if not os.path.isdir(CACHE):
        os.mkdir(CACHE)
    chapter_dir = BASE_DIR + '/chapters'
    if not os.path.isdir(chapter_dir):
        os.mkdir(chapter_dir)
    image_dir = BASE_DIR + '/images'
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)


def main():
    prepare()
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
        topic = chapter.split('/')[1]
        topic_dir = BASE_DIR + '/' + topic
        if not os.path.isdir(topic_dir):
            os.mkdir(topic_dir)
        html_doc = download(chapter)
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.title.text.split('|')[1].strip().replace(' Documentation', '')
        article_body = soup.find('div', {'class': 'devsite-article-body'})
        cards = article_body.find_all('div', {'class': 'card'})
        print('\\chapter{' + title + '}')
        links = [l for l in article_body.find_all('a')]
        for card in cards:
            links = card.find_all('a')
            for link in links:
                print(link.attrs['href'])
                parse(topic, link.attrs['href'])


main()

import os
import subprocess

import requests
from bs4 import BeautifulSoup

from lib.DocumentParser import DocumentParser
from lib.KeyCreator import KeyCreator


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
            outimage.write(''.join(parser.get_nodes()).replace(' .', '.').encode('utf-8').decode('ascii',
                                                                                                 errors='replace').replace(
                '�', '?'))
        fetch_images(parser.get_images())
        create_index(articles)


def main():
    foo = [
        'https://cloud.google.com/compute/docs/concepts',
        'https://cloud.google.com/iam/docs/concepts',
        'https://cloud.google.com/dlp/docs/concepts',
        'https://cloud.google.com/vpc/docs/concepts',
        'https://cloud.google.com/storage/docs/concepts',
        'https://cloud.google.com/identity/docs/concepts',
        'https://cloud.google.com/sql/docs/concepts',
    ]
    for f in foo:
        key = f.split('/')[3]
        r = requests.get(f, allow_redirects=True)
        html_doc = r.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.title.text.split('|')[0].strip()
        article = soup.find('div', {'class': 'devsite-article-body'})
        links = article.find_all('a')
        print(links)
        print(key)
        exit(1)
    chapters = [
        {
            'title': 'Cloud Virtual Private Network',
            'directory': 'chapters/vpc/',
            'articles': [
                'https://cloud.google.com/vpc/docs/overview',
                'https://cloud.google.com/vpc/docs/vpc',
                'https://cloud.google.com/vpc/docs/firewalls',
                'https://cloud.google.com/vpc/docs/firewall-rules-logging',
                'https://cloud.google.com/vpc/docs/routes',
                'https://cloud.google.com/vpc/docs/advanced-vpc',
                'https://cloud.google.com/vpc/docs/legacy',
                'https://cloud.google.com/vpc/docs/shared-vpc',
                'https://cloud.google.com/vpc/docs/vpc-peering',
                'https://cloud.google.com/compute/docs/ip-addresses',
                'https://cloud.google.com/vpc/docs/alias-ip',
                'https://cloud.google.com/vpc/docs/multiple-interfaces-concepts',
                'https://cloud.google.com/vpc/docs/packet-mirroring',
                'https://cloud.google.com/vpc/docs/private-access-options',
            ]
        },
        {
            'title': 'Cloud Data Loss Prevention',
            'directory': 'chapters/dlp/',
            'articles': [
                'https://cloud.google.com/dlp/docs/concepts-actions',
                'https://cloud.google.com/dlp/docs/concepts-image-redaction',
                'https://cloud.google.com/dlp/docs/infotypes-reference',
                'https://cloud.google.com/dlp/docs/concepts-job-triggers',
                'https://cloud.google.com/dlp/docs/likelihood',
                'https://cloud.google.com/dlp/docs/classification-redaction',
                'https://cloud.google.com/dlp/docs/concepts-date-shifting',
                'https://cloud.google.com/dlp/docs/concepts-bucketing',
                'https://cloud.google.com/dlp/docs/pseudonymization',
                'https://cloud.google.com/dlp/docs/concepts-text-redaction',
                'https://cloud.google.com/dlp/docs/concepts-risk-analysis',
                'https://cloud.google.com/dlp/docs/concepts-templates',
            ]
        }
    ]
    for articles in chapters:
        parse(articles)


main()

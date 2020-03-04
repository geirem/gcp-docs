from typing import Optional, List

from bs4 import BeautifulSoup, PageElement, NavigableString

from lib.KeyCreator import KeyCreator
from lib.ParsingStrategy import ParsingStrategy


class DocumentParser:

    def __init__(self, document: str, key_creator: KeyCreator):
        self._key_creator = key_creator
        self._parsed_elements = []
        self._contents = self.__extract_document(document)
        self.__images = []
        self._parsing_strategy = ParsingStrategy(key_creator, self.__images)

    def __extract_document(self, document: str) -> Optional[PageElement]:
        soup = BeautifulSoup(document, 'html.parser')
        title = soup.title.text.split('|')[0].strip()
        self._parsed_elements.append('\\section{' + title + '}\n')
        return soup.find('div', {'class': 'devsite-article-body'})

    @staticmethod
    def _apply_html_entities(processed: Optional[str]) -> str:
        if processed is None:
            return ''
        return processed.encode(encoding='ascii', errors='xmlcharrefreplace').decode('utf-8')

    def parse(self):
        self.__parse_node(self._contents)

    def __parse_node(self, node: PageElement):
        tag = self._parsing_strategy.get_parser(node).parse(node)
        if tag['open'] is not None:
            self._parsed_elements.append(tag['open'])
        for child in DocumentParser.__get_children(node):
            self.__parse_node(child)
        if tag['close'] is not None:
            self._parsed_elements.append(tag['close'])

    @staticmethod
    def __get_children(node: PageElement):
        return [] if type(node) is NavigableString else node.children

    def get_nodes(self):
        nodes = []
        node_count = len(self._parsed_elements)
        i = 0
        while i < node_count:
            e = self._parsed_elements[i]
            i += 1
            if e == '':
                continue
            if 'Read more about' in e:
                i += 4
                nodes.append('\n')
                continue
            nodes.append(e)
        return nodes

    def get_images(self) -> List[dict]:
        return self.__images

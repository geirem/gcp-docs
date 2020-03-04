import importlib
import os
import pkgutil

from bs4 import NavigableString

from lib.KeyCreator import KeyCreator
from lib.TagParser import TagParser


class ParsingStrategy:

    def __init__(self, key_creator: KeyCreator, images: list):
        self.__parsers = {}
        for (_, name, _) in pkgutil.iter_modules([os.path.dirname(__file__) + '/parsers']):
            imported_module = importlib.import_module('lib.parsers.' + name)
            clazz_name = list(filter(lambda x: x != 'TagParser' and not x.startswith('__'), dir(imported_module)))[0]
            clazz = getattr(imported_module, clazz_name)
            self.__parsers[self.__key_from_name(clazz_name)] = clazz(key_creator, images)
        self.__default_parser = TagParser(key_creator, images)

    @staticmethod
    def __key_from_name(name: str) -> str:
        return name.replace('Parser', '').lower()

    def get_parser(self, node) -> TagParser:
        node_name = 'navigablestring' if type(node) is NavigableString else node.name
        return self.__parsers.get(node_name, self.__default_parser)

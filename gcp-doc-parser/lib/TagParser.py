from typing import Optional

from lib import KeyCreator


class TagParser:

    def __init__(self, key_creator: KeyCreator, images: list):
        self._key_creator = key_creator
        self._images = images

    def parse(self, node) -> dict:
        if type(self) is TagParser:
            name = node.name
            if name is not None:
                print(name)
            return {
                'open': node.name.upper() + ': ',
                'close': None,
            }
        return {
            'open': None,
            'close': None,
        }

    @staticmethod
    def _text(node) -> str:
        text = node.text.strip()
        text = ' '.join(text.split())
        return text

    @staticmethod
    def _peek_at_first_child(node) -> Optional[dict]:
        children = node.children
        if len(children) == 0:
            return None
        return children[0]

from lib.TagParser import TagParser


class NavigableStringParser(TagParser):

    def parse(self, node) -> dict:
        text = ' '.join(node.strip().split())
        text = text.replace('_', '\\_')
        text = text.replace('%', '\\%')
        return {
            'open': text,
            'close': None, #'\n\n',
        }


from lib.TagParser import TagParser


class BrParser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': '\n\n',
            'close': None,
        }

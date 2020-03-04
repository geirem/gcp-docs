from lib.TagParser import TagParser


class LiParser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': '\\item ',
            'close': '\n',
        }

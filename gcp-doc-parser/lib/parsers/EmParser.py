from lib.TagParser import TagParser


class EmParser(TagParser):

    def parse(self, item) -> dict:
        return {
            'open': '{\\sl ',
            'close': '}\n',
        }

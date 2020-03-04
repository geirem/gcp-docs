from lib.TagParser import TagParser


class StrongParser(TagParser):

    def parse(self, item) -> dict:
        return {
            'open': '{\\sl ',
            'close': '}\n',
        }

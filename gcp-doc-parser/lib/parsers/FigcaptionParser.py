from lib.TagParser import TagParser


class FigcaptionParser(TagParser):

    def parse(self, node) -> dict:
        return {
            'open': '\\caption{',
            'close': '}\n',
        }

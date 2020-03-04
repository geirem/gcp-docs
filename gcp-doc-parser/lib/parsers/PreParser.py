from lib.TagParser import TagParser


class PreParser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': ' \\begin{verbatim}\n',
            'close': '\\end{verbatim}\n',
        }

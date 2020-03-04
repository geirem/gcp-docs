from lib.TagParser import TagParser


class H2Parser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': '\\subsection{',
            'close': '}\n',
        }

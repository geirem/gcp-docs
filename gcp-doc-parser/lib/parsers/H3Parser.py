from lib.TagParser import TagParser


class H3Parser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': '\\subsubsection{',
            'close': '}\n',
        }

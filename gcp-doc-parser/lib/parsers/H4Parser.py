from lib.TagParser import TagParser


class H4Parser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': '\\subsubsection{',
            'close': '}\n',
        }

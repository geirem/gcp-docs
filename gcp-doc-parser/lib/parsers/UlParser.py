from lib.TagParser import TagParser


class UlParser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': '\\begin{itemize}',
            'close': '\\end{itemize}\n',
        }

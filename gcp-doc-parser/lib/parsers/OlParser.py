from lib.TagParser import TagParser


class OlParser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        return {
            'open': '\\begin{enumerate}',
            'close': '\\end{enumerate}\n',
        }

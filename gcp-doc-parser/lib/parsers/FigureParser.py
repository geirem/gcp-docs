from lib.TagParser import TagParser


class FigureParser(TagParser):

    def parse(self, node) -> dict:
        return {
            'open': '\n\\begin{figure}\n\\centering\n',
            'close': '\n\\end{figure}\n',
        }

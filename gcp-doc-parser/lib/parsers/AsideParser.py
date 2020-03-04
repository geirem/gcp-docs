from lib.TagParser import TagParser


class AsideParser(TagParser):
    def parse(self, item) -> dict:
        return {
            'open': '\\begin{figure}[h]\n\\centering\n\\begin{minipage}{0.8\\textwidth}\n\\centering\n',
            'close': '\n\\end{minipage}\n\\end{figure}\n',
        }

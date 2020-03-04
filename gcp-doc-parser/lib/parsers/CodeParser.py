from lib.TagParser import TagParser


class CodeParser(TagParser):

    # noinspection PyUnusedLocal
    def parse(self, node) -> dict:
        if node.parent.name in ('h1', 'h2', 'h3', 'h4'):
            return super().parse(node)
        return {
            'open': ' \\verb|',
            'close': '| ',
        }

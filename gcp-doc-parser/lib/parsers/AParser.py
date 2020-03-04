from lib.TagParser import TagParser


class AParser(TagParser):

    def parse(self, node) -> dict:
        return {
            'open': ' ',#\\href{' + href + '}{',
            'close': '', #'}',
        }

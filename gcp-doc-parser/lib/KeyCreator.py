class KeyCreator:

    def __init__(self, prefix: str):
        self.__prefix = prefix

    def key(self, document_name: str) -> str:
        key = document_name.split('/').pop()
        if key == '' or key is None:
            key = 'index'
        return self.__prefix + '_' + key

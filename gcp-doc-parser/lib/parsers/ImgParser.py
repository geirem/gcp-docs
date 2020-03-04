from lib.TagParser import TagParser


class ImgParser(TagParser):

    def parse(self, item) -> dict:
        image_src = item.attrs['src']
        image = {
            'src': image_src,
            'src_name': 'images/' + self._key_creator.key(image_src),
        }
        image['name'] = image['src_name'].replace('.svg', '.eps').replace('.png', '.eps').replace('.jpg', '.eps')
        self._images.append(image)
        return {
            'open': '\\includegraphics[width=0.5\\textwidth]{' + image['name'] + '}',
            'close': '\n',
        }

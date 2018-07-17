import json


class Node:

    tag_tmp = '<{tag}>{content}</{tag}>'

    def __init__(self, dict_of_tags):

        self.dict_of_tags = dict_of_tags

    def render(self):

        arr = []

        for tag, content in self.dict_of_tags.items():
            snippet = self.tag_tmp.format(tag=tag, content=content)
            arr.append(snippet)

        return ''.join(arr)


class Parser:

    def parse(self, json_doc):

        # import ipdb; ipdb.set_trace()
        parsed = json.loads(json_doc, object_hook=self._object_hook)

        return ''.join(parsed)

    def _object_hook(self, obj):

        node = Node(obj)
        return node.render() # NOTE лучше возвращать саму ноду и потом вручную отрендерить в списке. При этом можно делать местные проверки.


def main():

    json_file = open('source.json', 'r')

    parser = Parser()
    print(parser.parse(json_file.read()))


if __name__ == '__main__':
    main()

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

    ul_tmp = '<ul>{content}</ul>'
    li_tmp = '<li>{content}</li>'

    def parse(self, json_doc):

        # import ipdb; ipdb.set_trace()
        parsed = json.loads(json_doc, object_hook=self._object_hook)

        li_list = []

        for item in parsed:
            li_item = self.li_tmp.format(content=item)
            li_list.append(li_item)

        return self.ul_tmp.format(content=''.join(li_list))

    def _object_hook(self, obj):

        node = Node(obj)
        return node.render() # NOTE лучше возвращать саму ноду и потом вручную отрендерить в списке. При этом можно делать местные проверки.


def main():

    json_file = open('source.json', 'r')

    parser = Parser()
    print(parser.parse(json_file.read()))


if __name__ == '__main__':
    main()

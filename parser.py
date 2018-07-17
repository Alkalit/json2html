import json

from collections import OrderedDict


class MyCustomDecoder(json.JSONDecoder):

    """
    Базовый класс декодера не предоставляет хука для типа списка, исправим это недоразуменее.

    Честно украдено отсюда:
    https://stackoverflow.com/questions/10885238/python-change-list-type-for-json-decoding
    """

    def __init__(self, list_type=list,  **kwargs):
        super(MyCustomDecoder, self).__init__(**kwargs)

        # Use the custom JSONArray
        self.parse_array = self.JSONArray

        # Use the python implemenation of the scanner
        self.scan_once = json.scanner.py_make_scanner(self)
        self.list_type=list_type

    def JSONArray(self, s_and_end, scan_once, **kwargs):
        values, end = json.decoder.JSONArray(s_and_end, scan_once, **kwargs)
        return self.list_type(values), end


class ListNode:

    ul_tmp = '<ul>{content}</ul>'
    li_tmp = '<li>{content}</li>'

    def __init__(self, list_of_tags):

        self.list_of_tags = list_of_tags

    def render(self):

        li_list = []

        for node in self.list_of_tags:
            li_item = node.render()
            li_item = self.li_tmp.format(content=li_item)
            li_list.append(li_item)

        return self.ul_tmp.format(content=''.join(li_list))


class Node:

    tag_tmp = '<{tag}>{content}</{tag}>'

    def __init__(self, dict_of_tags):

        self.dict_of_tags = dict_of_tags

    def render(self):

        arr = []

        for tag, content in self.dict_of_tags.items():

            if  isinstance(content, ListNode):
                content = content.render()

            snippet = self.tag_tmp.format(tag=tag, content=content)
            arr.append(snippet)

        return ''.join(arr)


class Parser:

    def parse(self, json_doc):

        parsed = json.loads(json_doc, cls=MyCustomDecoder, object_pairs_hook=self._object_hook, list_type=ListNode)

        # import ipdb; ipdb.set_trace()
        return parsed.render()

    def _object_hook(self, obj):

        # import ipdb; ipdb.set_trace()

        node = Node(OrderedDict(obj)) # XXX или вынести это в саму ноду?
        return node#.render() # NOTE лучше возвращать саму ноду и потом вручную отрендерить в списке. При этом можно делать местные проверки.


def main():

    json_file = open('source.json', 'r')

    parser = Parser()
    print(parser.parse(json_file.read()))


if __name__ == '__main__':
    main()

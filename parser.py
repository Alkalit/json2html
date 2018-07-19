import json
import abc
import re

from html import escape
from collections import OrderedDict, namedtuple


TAG_REGEX = r"^[a-z][a-z_0-9]*"
ID_REGEX = r"#[a-z1-9][a-z0-9_-]*"
CLASS_REGEX = r"\.[a-z1-9][a-z0-9_-]*"

IDENTIFICATOR = r"\.|#"

TOKEN_SPECIFICATION = [
    ('TAG', TAG_REGEX),        # AN HTML TAG
    ('ID', ID_REGEX),          # A CSS ID
    ('CLASS', CLASS_REGEX),    # A CSS class
]

TOKEN_REGEX = "|".join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)

TOKEN_PATTERN = re.compile(TOKEN_REGEX, re.I)
IDENTIFICATOR_PATTERN = re.compile(IDENTIFICATOR, re.I)

KeyToken = namedtuple('KeyToken', ['type', 'value'])

def tokenize_key(key):

    line_num = 1
    line_start = 0

    for match_object in TOKEN_PATTERN.finditer(key):
        type_ = match_object.lastgroup
        value = match_object.group(type_)

        column = match_object.start() - line_start

        yield KeyToken(type_, value)


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


class BaseNode(abc.ABC):

    """
    Просто показываем что ноды это родственные классы.
    """

    @abc.abstractmethod
    def render(self):
        pass


class ListNode(BaseNode):

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


class Node(BaseNode):

    tag_tmp = '<{opening_tag}>{content}</{closing_tag}>'

    def __init__(self, dict_of_tags):

        self.dict_of_tags = dict_of_tags

    def render(self):

        arr = []

        for tag, content in self.dict_of_tags.items():

            if isinstance(content, ListNode):
                content = content.render()

            elif isinstance(content, str):
                content = escape(content)

            ids = ''
            classes = ''

            # в противном случае будем парсить каждый тег в json-объекте
            if IDENTIFICATOR_PATTERN.search(tag):

                for token in tokenize_key(tag):
                    if token.type == 'TAG' and token.value != tag:
                        tag = token.value

                    elif token.type == 'ID':
                        # ids.append(token.value[1:])
                        ids = " ".join([ids, token.value[1:]])

                    elif token.type == 'CLASS':
                        # classes.append(token.value[1:])
                        classes = " ".join([classes, token.value[1:]])

                if classes:
                    classes = "class=\"{}\"".format(classes.strip())

                if ids:
                    ids = "id=\"{}\"".format(ids.strip())

            closing_tag = tag
            opening_tag = " ".join([tag, classes, ids])

            snippet = self.tag_tmp.format(opening_tag=opening_tag.strip(), content=content, closing_tag=closing_tag)
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

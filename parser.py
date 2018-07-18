import json
import abc
import re

from html import escape
from collections import OrderedDict

TAG = r'^[a-z][a-z_0-9]*'
CSS_SELECTOR = r"[.#][a-z][a-z0-9_-]*"

tag_regex = re.compile(TAG)
css_selector_regex = re.compile(CSS_SELECTOR)

def parse_key(key):

    # Не гуру регулярок, поэтому парсим полу-вручную

    result = {}

    matched_tag = tag_regex.match(key)

    if not matched_tag:
        raise Exception("The key \"{key}\" is an invalid key".format(key))

    tag = matched_tag.group()

    # далее ищем классы и айдишники
    key = key[matched_tag.end():]

    selectors = css_selector_regex.finditer(key)

    ids = []
    classes = []

    for matcher in selectors:
        select = matcher.group()

        if select.startswith('.'):
            classes.append(select[1:])
        elif select.startswith('#'):
            ids.append(select[1:])
        else:
            pass # TODO should I deal with it?

    # import ipdb; ipdb.set_trace()
    result['tag'] = tag

    if classes:
        result['classes'] = classes
    if ids:
        result['ids'] = ids

    return result


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

            # import ipdb; ipdb.set_trace()
            parsed_tag = parse_key(tag)

            if parsed_tag['tag'] != tag:
                ids = parsed_tag.get('ids', '')
                classes = parsed_tag.get('classes', '')

                if classes:
                    classes = "class=\"{}\"".format(" ".join(classes))

                if ids:
                    ids = "id=\"{}\"".format(" ".join(ids))

                closing_tag = parsed_tag['tag']
                opening_tag = " ".join([closing_tag, classes, ids])
            else:
                opening_tag = tag
                closing_tag = tag

            snippet = self.tag_tmp.format(opening_tag=opening_tag, content=content, closing_tag=closing_tag)
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

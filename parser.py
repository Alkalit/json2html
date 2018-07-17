import json


class Node:

    title_tmp = '<h1>{}</h1>'
    body_tmp = '<p>{}</p>'

    def __init__(self, title, body):

        self.title = title
        self.body = body

    def render(self):

        return ''.join([self.title_tmp.format(self.title), self.body_tmp.format(self.body)])


class Parser:

    def parse(self, json_doc):

        # import ipdb; ipdb.set_trace()
        parsed = json.loads(json_doc, object_hook=self._object_hook)

        return ''.join(parsed)

    def _object_hook(self, obj):

        node = Node(**obj)
        return node.render()

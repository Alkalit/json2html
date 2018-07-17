import unittest

from ..parser import Parser, Node


class TestParser(unittest.TestCase):

    def test_markup(self):

        json_doc = """
            [
                {
                    "title": "Title #1",
                    "body": "Hello, World 1!"
                },
                {
                    "title": "Title #2",
                    "body": "Hello, World 2!"
                }
            ]
        """

        expected = "<h1>Title #1</h1><p>Hello, World 1!</p><h1>Title #2</h1><p>Hello, World 2!</p>"

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_obj_hook(self):
        pass


class TestNode(unittest.TestCase):

    def test_node_can_render_it_self(self):

        args = dict(title='Foo', body='Bar')

        node = Node(**args)

        rendered = node.render()
        expected = '<h1>Foo</h1><p>Bar</p>'

        self.assertEqual(rendered, expected)

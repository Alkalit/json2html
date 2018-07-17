import unittest

from ..parser import Parser, Node


class TestParser(unittest.TestCase):

    def test_markup(self):

        json_doc = """
            [
                {
                    "h3": "Title #1",
                    "div": "Hello, World 1!"
                },
                {
                    "h2": "Title #2",
                    "p": "Hello, World 2!"
                },
                {
                    "h1": "Title #3",
                    "b": "Hello, World 3!"
                }
            ]
        """

        expected = "<h3>Title #1</h3><div>Hello, World 1!</div><h2>Title #2</h2><p>Hello, World 2!</p><h1>Title #3</h1><b>Hello, World 3!</b>"

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_obj_hook(self):
        pass


class TestNode(unittest.TestCase):

    def test_node_can_render_it_self(self):

        tags = dict(title='Foo', body='Bar')

        node = Node(tags)

        rendered = node.render()
        expected = '<title>Foo</title><body>Bar</body>'

        self.assertEqual(rendered, expected)

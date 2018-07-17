import unittest

from ..parser import Parser, Node, ListNode


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

        expected = "<ul><li><h3>Title #1</h3><div>Hello, World 1!</div></li><li><h2>Title #2</h2><p>Hello, World 2!</p></li><li><h1>Title #3</h1><b>Hello, World 3!</b></li></ul>"

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


class TestListNode(unittest.TestCase):

    def test_node_can_render_it_self(self):

        node1 = Node({"h1":"Hi there!", "h2":"How do you do?"})
        node2 = Node(dict(h3='a title', div='a content'))

        list_node = ListNode([node1, node2])
        rendered = list_node.render()
        expected = '<ul><li><h1>Hi there!</h1><h2>How do you do?</h2></li><li><h3>a title</h3><div>a content</div></li></ul>'

        self.assertEqual(rendered, expected)

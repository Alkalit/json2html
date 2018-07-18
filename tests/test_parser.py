import unittest

from ..parser import Parser, Node, ListNode, parse_key


class TestParser(unittest.TestCase):

    def test_escape_inner_html(self):

        json_doc = """
            {
                "p": "a <a>link</a>"
            }
        """

        expected = "<p>a &lt;a&gt;link&lt;/a&gt;</p>"

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_render_an_object_with_css_keys(self):

        json_doc = """
            {
                "p.my-class#my-id": "hello",
                "p.my-class1.my-class2": "example"
            }
        """

        expected = """<p class="my-class" id="my-id">hello</p><p class="my-class1 my-class2" >example</p>"""

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_render_with_a_simple_object(self):

        json_doc = """
            {
                "p": "hello1"
            }
        """

        expected = "<p>hello1</p>"

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_render_with_a_list_with_a_simple_object(self):

        json_doc = """
            [
                {
                    "div": "div 1"
                }
            ]
        """

        expected = "<ul><li><div>div 1</div></li></ul>"

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_render_with_nested_list(self):

        json_doc = """
            [
                {
                    "span": "Title #1",
                    "content": [
                        {
                            "p": "Example 1",
                            "header": "header 1"
                        }
                    ]

                }
            ]
        """

        expected = "<ul><li><span>Title #1</span><content><ul><li><p>Example 1</p><header>header 1</header></li></ul></content></li></ul>"

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_render_with_deep_nesting(self):

        json_doc = """
            [
                {
                    "h1": "Title #1",
                    "div": [
                        {
                            "div": [
                                {
                                    "h2": "Title #2",
                                    "div": [
                                        {
                                            "div": [
                                                {
                                                    "h3": "Title #3",
                                                    "div": [
                                                        {
                                                            "p": "some text"
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        """

        expected = "<ul><li><h1>Title #1</h1><div><ul><li><div><ul><li><h2>Title #2</h2><div><ul><li><div><ul><li><h3>Title #3</h3><div><ul><li><p>some text</p></li></ul></div></li></ul></div></li></ul></div></li></ul></div></li></ul></div></li></ul>"

        json2html_parser = Parser()
        parsed = json2html_parser.parse(json_doc)

        self.assertEqual(expected, parsed)

    def test_render_with_a_few_objects(self):

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


class TestKeyParser(unittest.TestCase):

    def test_key_parser_with_no_identety(self):

        key = 'h1'

        result = parse_key(key)

        expected = {"tag":'h1'}

        self.assertEqual(result, expected)

    def test_key_parser_with_a_css_class(self):

        key = 'p.my-class'

        result = parse_key(key)

        expected = {"tag":'p', "classes": ['my-class']}

        self.assertEqual(result, expected)

    def test_key_parser_with_a_css_id(self):

        key = 'p#my-id'

        result = parse_key(key)

        expected = {"tag":'p', "ids": ['my-id']}

        self.assertEqual(result, expected)

    def test_key_parser_with_multiple_attrs(self):

        key = 'p.my-class#my-id.my_class1#my_id1'

        result = parse_key(key)

        expected = {"tag":'p', "ids": ['my-id', 'my_id1'], "classes": ['my-class', 'my_class1']}

        self.assertEqual(result, expected)

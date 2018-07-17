import unittest

from ..parser import Parser


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

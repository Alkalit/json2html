import json


class Parser:

    title_tmp = '<h1>{}</h1>'
    body_tmp = '<p>{}</p>'

    def parse(self, json_doc):

        parsed = json.loads(json_doc)

        html_tags = []

        for obj in parsed:
            title = obj['title']
            html_tags.append(self.title_tmp.format(title))

            body = obj['body']
            html_tags.append(self.body_tmp.format(body))


        return ''.join(html_tags)

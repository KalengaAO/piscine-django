#!/usr/bin/python3

class Text(str):

    def __str__(self):
        text = super().__str__().replace('<', '&lt;').replace('>', '&gt;')
        if text == '"':
            text = text.replace('"', '&quot;')
        return text.replace('\n', '\n<br />\n')

class Elem:

    class ValidationError(Exception):
        def __init__(self, message="It's neither a text nor an Elem"):
            super().__init__(message)

    def __init__(self, tag='div', attr={}, content=None, tag_type='double'):
        self.tag = tag
        self.attr = attr
        self.content = []
        if content:
            self.add_content(content)
        elif content is not None and not isinstance(content, Text):
            raise self.ValidationError 
        self.tag_type = tag_type

    def __str__(self):
        result = ""
        if self.tag_type == 'double':
            result = "<{0}{1}>{2}</{0}>".format(self.tag, self.__make__attr(), self.__make__content())
        elif self.tag_type == 'simple':
            result = "<{0}{1} />".format(self.tag, self.__make__attr())
        return result

    def __make__attr(self):
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make__content(self):
        if len(self.content) == 0:
            return ''
        result = '\n'
        for elem in self.content:
            result += "  " + str(elem).replace("\n", "\n  ") + "\n"
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        is_elem_instance = isinstance(content, Elem)
        is_text = type(content) == Text
        is_elem_list = type(content) ==  list and all([isinstance(elem, Elem) or type(elem) == Text for elem in content])
        requirements = [is_elem_instance, is_text, is_elem_list]
        return any(requirements)

if __name__ == "__main__":
    elem = Elem(tag='html', content=[
        Elem(tag='head', content=Elem(tag='title', content=Text('"Hello ground!"'))),
        Elem(tag='body', content=[ 
            Elem(tag='h1', content=Text('"Oh no, not again!"')),
            Elem(tag='img', tag_type='simple', attr={'src':'http://i.imgur.com/pfp3T.jpg'})
        ])
    ])
    print(elem)

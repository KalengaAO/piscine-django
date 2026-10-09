from elements import (H1, H2, Body, Div, Elem, Head, Hr, Html, Img,
            Li, Meta, Ol, P, Span, Table, Td, Text, Th, Title, Tr, Ul)


ALLOWED_TAGS = (H1, H2, Body, Div, Elem, Head, Hr, Html, Img,
            Li, Meta, Ol, P, Span, Table, Td, Text, Th, Title, Tr, Ul)

HTML_CONTENT = (Head, Body)
HEAD_CONTENT = (Title)
BODY_CONTENT = DIV_CONTENT = (H1, H2, Div, Table, Ul, Ol, Span, Text, P)
TITLE_CONTENT = H1_CONTENT = H2_CONTENT = LI_CONTENT = TH_CONTENT = TD_CONTENT = P_CONTETN = (Text)
SPAC_CONTENT = (Text, P)
UL_CONTENT = OL_CONTENT = (Li)
TR_CONTENT = (Th, Td)
TABLE_CONTENT = (Tr)

class Page:
    def __init__(self, elem):
        if not isinstance(elem, (Elem, Text)):
            raise Elem.ValidationError 
        self.elem = elem
        self._error_msg = None


    @property
    def error_msg(self):
        if self._error_msg:
            return self._error_msg
        else:
            return "No errors"

    @error_msg.setter
    def error_msg(self, message):
        if self._error_msg is None:
            self._error_msg = message

    def __str__(self):
        result = ""
        if isinstance(self.elem, Html):
            result += "<!DOCTYPE html>\n"
        result += str(self.elem)
        return result
    
    def write_to_file(self, path):
        with open(path, 'w') as file:
            file.write(self.__str__())

    def is_valid(self):
        return self.__recursive_check(self.elem)

    def check_subelem(self, elem, instance_list=None):
        if instance_list:
            if (all(isinstance(e, instance_list) for e in elem.content)):
                return True
            else:
                return False
        elif (all(self.__recursive_check(e) for e in elem.content)):
            return True
        return False

    def __recursive_check(self, elem):
        if not (isinstance(elem, ALLOWED_TAGS)):
            return False

        if isinstance(elem, Html):
            if len(elem.content) == 2 and isinstance(elem.content[0], Head) \
                and isinstance(elem.content[1], Body):
                if self.check_subelem(elem):
                    return True
            else:
                self.error_msg = (f"{elem.tag} tag must striclty contain a Head, then a Body")
        elif isinstance(elem, Head):
            if [isinstance(e, Title) for e in elem.content].count(True) == 1:
                return True
            else:
                self.error_msg = (f"{elem.tag} Tag Head must only contain one Title and at least a Title")
                
        elif isinstance(elem, (Body, Div)):
            if self.check_subelem(elem, BODY_CONTENT) and self.check_subelem(elem):
                return True
            else:
                self.error_msg = (f"{elem.tag} tag must only contain the following type of elements: {BODY_CONTENT}")

        elif isinstance(elem, (Title, H1, H2, Li, Th, Th, Td)):
            if len(elem.content) == 1 and isinstance(elem.content[0], Text):
                return True
            else:
                self.error_msg = (f"{elem.tag} tag must contain only Text")
        elif isinstance(elem, P):
            if self.check_subelem(elem, P_CONTETN):
                return True
            else:
                self.error_msg = (f"{elem.tag} tag must contain Text.")
        elif isinstance(elem, Span):
            if self.check_subelem(elem, SPAC_CONTENT) and \
                self.check_subelem(elem):
                return True
            else:
                self.error_msg = (f"{elem.tag} tag must only contain Text or some P")
        elif isinstance(elem, (Ul, Ol)):
            if len(elem.content) > 0 and self.check_subelem(elem, UL_CONTENT) and self.check_subelem(elem):
                return True
            else:
                self.error_msg = (f"{elem.tag} tag must contain at least on Li and only some Li")
        elif isinstance(elem, Tr):
            if self.is_valid_tr(elem):
                return True
        elif isinstance(elem, Table):
            if all(isistance(e, Tr) for e in elem.content) and self.check_subelem(elem):
                return True
            else:
                self.error_msg = (f"{elem.tag} tag must only contain Tr and only some Tr.")
        return False

    def is_valid_tr(self, elem):
        if not (len(elem.content) > 0 and all(isinstance(e, (Th, Td)) for e in elem.content)):
            self.error_msg = (f"{elem.tag} tag must contain at least one Th or Td and only some Th or Td. "\
                "The Th and the Td must be mutually exclusive.")
            return False

            th_elements = [e for e in elem.content if isinstance(e, Th)]
            td_elements = [e for e in elem.content if isinstance(e, Td)]

            if len(th_elements) > 0 and len(td_elements) > 0:
                self.error_msg = (f"{elem.tag} tag must contain at least one Th or Td and only some Th or Td."\
                        "The Th and the Td must be mutually exclusive.")
                return False
            return True


if __name__ == "__main__":
    first_pag = Page(Html([Head([Meta(), Title(Text("first page"))]), \
    Body([H1(Text("My first pag html by python")), P(Text("não deve gerar um erro"))])]))

    if not first_pag.is_valid():
        print(first_pag.error_msg)
    else:
        first_pag.write_to_file("./index.html")

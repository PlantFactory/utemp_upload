
import xmltok

class Parser:
    def _get_name_from_token(self, token):
        name = None
        if token[1][0] == '':
            name = token[1][1]
        else:
            name = ':'.join(token[1])
        return name

    def parse(self, xml_string):
        self.dom = {}
        self.pis = {}
        current_tag = self.dom
        current_is_pi = False
        outer_tags = []
        current_pi = {}

        for token in xmltok.tokenize(xml_string):

            if token[0] == 'PI':
                current_is_pi = True
                current_pi = {}
                self.pis[token[1]] = current_pi

            elif token[0] == 'START_TAG':
                current_is_pi = False
                tag_name = self._get_name_from_token(token)

                outer_tags.append(current_tag)

                if tag_name in current_tag.keys() and not isinstance(current_tag[tag_name], list):
                    _child_tag = current_tag[tag_name]
                    current_tag[tag_name] = [_child_tag]
                    current_tag[tag_name].append({})
                    current_tag = current_tag[tag_name][-1]
                else:
                    current_tag[tag_name] = {}
                    current_tag = current_tag[tag_name]

            elif token[0] == 'ATTR':
                attr_name = self._get_name_from_token(token)
                attr_value = token[2]

                if current_is_pi:
                    current_pi.setdefault('$', {})
                    current_pi['$'][attr_name] = attr_value
                else:
                    current_tag.setdefault('$', {})
                    current_tag['$'][attr_name] = attr_value

            elif token[0] == 'TEXT':
                current_tag['_'] = token[1]

            elif token[0] == 'END_TAG':
                current_tag = outer_tags.pop()

            else:
                # Error
                pass

        return self.dom

class Builder:
    def build(self, xml_dict):
        self.xml = ''

        for tag in xml_dict.items():

            self._build(tag[0], tag[1])

        return self.xml

    def _build_attr(self, attr_dict):
        attr_text = ''

        for attr in attr_dict.items():
            attr_text += ' ' + attr[0] + '=\"' + attr[1] + '\"'

        return attr_text

    def _build(self, xml_tag, xml_dict):
        if not isinstance(xml_dict, list):
            xml_dict = [xml_dict]

        for child_xml_dict in xml_dict:
            self.xml += '<'
            self.xml += xml_tag

            if '$' in child_xml_dict.keys():
                self.xml += self._build_attr(child_xml_dict['$'])

            self.xml += '>'

            if '_' in child_xml_dict.keys():
                self.xml += child_xml_dict['_']

            for tag in child_xml_dict.items():
                if tag[0] in ['$', '_']:
                    continue

                # innerがさらにある時?
                self._build(tag[0], tag[1])

            self.xml += '</' + xml_tag + '>'

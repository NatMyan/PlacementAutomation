from Parser11 import Parser11

import re


class NetlistParser(Parser11):
    def __init__(self):
        self._elem_attributes = {}
        self._attributes_to_match = r'(m|w|l|nf|M|W|L|Nf|NF)\s*=\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)'
        self._required_attributes = {'m', 'l', 'w', 'nf'}

    def parse_input_file(self, lines):
        current_attributes = {}
        if lines:
            for line in lines:
                if not (line.startswith('+') or line.startswith('*') or line.startswith('.')):
                    match_token = re.match(r'(\S+)', line)
                    if match_token:
                        self._curr_token = match_token.group(1)
                        current_attributes = {}
                elif line.startswith('+'):
                    line = line[1:]

                for match in re.finditer(self._attributes_to_match, line):
                    attribute_name, attribute_value = match.groups()
                    current_attributes[attribute_name] = self._convert_to_number_type(attribute_value)

                if all(attr in current_attributes for attr in self._required_attributes):
                    self._elem_attributes[self._curr_token] = current_attributes

    def get_elem_attributes(self):
        return self._elem_attributes

    def _convert_to_number_type(self, attr_val):
        try:
            return int(attr_val)
        except ValueError:
            try:
                return float(attr_val)
            except ValueError:
                return attr_val

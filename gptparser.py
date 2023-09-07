from pyparsing import *
import json

class EU4Parser(object):

    def __init__(self):
        pass

    def parse_file(self, fileName):
        # Read input text from file
        with open(fileName, "r") as file:
            inputText = file.read()

        # Define parsing rules
        integer = Word(nums).setParseAction(lambda x: int(x[0]))
        float_num = Regex(r"[+-]?\d+\.\d*").setParseAction(lambda x: float(x[0]))
        quotedString.setParseAction(removeQuotes)
        unquotedString = Word(alphanums + "._-?\"")
        comment = "#" + restOfLine
        date_format = Combine(Word(nums) + "." + Word(nums) + "." + Word(nums))

        property_value = float_num | integer | date_format | quotedString | unquotedString
        property = Group(unquotedString + "=" + property_value)

        nested_object = Forward()
        nested_property = Group(unquotedString + "=" + nested_object)
        nested_object << ("{" + OneOrMore(nested_property | property | comment) + "}")

        parsed_objects = OneOrMore(nested_property | property + Optional(comment))

        parsed_objects.ignore(comment)

        parsed_list = parsed_objects.parseString(inputText, parseAll=True)
        print(parsed_list)

        # Convert to dictionary
        parsed_dict = self.convert_to_dict(parsed_list)
        return json.dumps(parsed_dict, indent=4)

    def convert_to_dict(self, input_list):
        result = {}
        for obj in input_list:
            key = obj[0]
            value = obj[2]

            property_dict = {}
            for prop in properties:
                prop_name, prop_value = prop[0], prop[1]

                if isinstance(prop_value, list):
                    prop_value = self.convert_to_dict(prop_value)

                if prop_name in property_dict:
                    if isinstance(property_dict[prop_name], list):
                        property_dict[prop_name].append(prop_value)
                    else:
                        property_dict[prop_name] = [property_dict[prop_name], prop_value]
                else:
                    property_dict[prop_name] = prop_value

            result[key] = property_dict

        return result

if __name__ == "__main__":
    parser = EU4Parser()
    parsed_dict = parser.parse_file("foo.txt")
    print(parsed_dict)

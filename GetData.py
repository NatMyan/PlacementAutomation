import InputReader
from NetlistParser import NetlistParser
from JSONParser import JSONParser


def getLinesFromInput(file_name):
    input_reader = InputReader.InputReader(file_name)
    lines = input_reader.read_input()
    return lines


def getNetlistDetails(file_name):
    netlistDict = {}
    if file_name:
        lines = getLinesFromInput(file_name)

        parser = NetlistParser()
        parser.parse_input_file(lines)
        attributes = parser.get_elem_attributes()
        for name, attributeList in attributes.items():
            if attributeList != {}:
                netlistDict[name] = attributeList

    return netlistDict


def getJSONDetails(file_name):
    jsonDict = {}
    if file_name:
        lines = getLinesFromInput(file_name)

        parser = JSONParser()
        parser.parse_input_file(lines)
        data = parser.get_data()
        for name, transistorList in data.items():
            if data:
                jsonDict[name] = transistorList

    return jsonDict

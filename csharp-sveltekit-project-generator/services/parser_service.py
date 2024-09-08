from typing import Tuple
import xml.etree.ElementTree as ET
import helpers.util as util
from domain.entity_class import EntityClass
from domain.entity_property import EntityProperty

xml_root = None


def parse(path: str) -> list[EntityClass]:
    global xml_root
    xml_root = _read_xml_document(path)
    return _process_xml(xml_root)


def _read_xml_document(path: str):
    try:
        print(f"Reading XML document from: {path}")
        with open(path, "r") as file:
            print(f"Successfully read XML document from: {path}")
            return ET.parse(file).getroot()
    except FileNotFoundError:
        print(f"File not found: {path}")
        exit(-1)


def _process_xml(xml_root) -> list[EntityClass]:
    classes: list[EntityClass] = []
    classes.extend(_process_classes(xml_root))
    return classes


def _process_classes(xml_root) -> list[EntityClass]:
    print("Processing classes...")
    classes: list[EntityClass] = []
    xml_classes = xml_root.findall(
        ".//packagedElement[@xmi:type='uml:Class']", util.NAMESPACES
    )
    for fmclass in xml_classes:
        if fmclass == None:
            continue

        parsed_class = _parse_class(fmclass)
        classes.append(parsed_class)
    print(f"Processed {len(classes)} classes.")
    return classes


def _parse_class(fmclass) -> EntityClass:
    class_name = fmclass.get("name")
    print(f"Processing class: {class_name}")
    attributes = _parse_class_attributes(fmclass, class_name)
    return EntityClass(class_name, attributes)


def _parse_class_attributes(fmclass, class_name: str) -> list[EntityProperty]:
    print(f"Processing class attributes: {class_name}")
    attributes: list[EntityProperty] = []
    attributes_elements = fmclass.findall(".//ownedAttribute", util.NAMESPACES)
    for attribute in attributes_elements:
        parsed_attribute = _parse_attribute(attribute)
        if parsed_attribute != None:
            attributes.append(parsed_attribute)
    return attributes


def _parse_attribute(attribute) -> EntityProperty | None:
    attribute_name = attribute.get("name")
    if attribute_name == None or attribute_name == "id":
        return None
    attribute_type, is_single_reference, is_reference = _parse_attribute_type(attribute)
    return EntityProperty(
        attribute_name, attribute_type, is_single_reference, is_reference
    )


def _parse_attribute_type(attribute) -> Tuple[str, bool, bool]:
    global xml_root
    is_single_reference = False
    is_reference = False
    try:
        if xml_root == None:
            return "object"

        type_id = attribute.attrib["type"]
        element = xml_root.find(
            ".//packagedElement[@xmi:id='{}']".format(type_id), util.NAMESPACES
        )
        reference_element_type = attribute.find(".//upperValue[@value]")
        cardinality = reference_element_type.attrib["value"]
        is_reference = True
        data_type_name = element.attrib["name"]
        if cardinality != "*":
            is_single_reference = True
    except KeyError:
        element = attribute.find(
            ".//type/xmi:Extension/referenceExtension", util.NAMESPACES
        )
        type_string_raw = element.attrib["referentPath"]
        uml_type = type_string_raw.split("::")[-1]
        data_type_name = util.CSHARP_TYPE_MAPPER[uml_type]

    return data_type_name, is_single_reference, is_reference

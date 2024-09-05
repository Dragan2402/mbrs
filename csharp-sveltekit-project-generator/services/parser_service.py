import xml.etree.ElementTree as ET
import helpers.util as util


def parse(path: str):
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


def _process_xml(xml_root):
    classes = []
    classes.extend(_process_classes(xml_root))


def _process_classes(xml_root):
    print("Processing classes...")
    classes = []
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


def _parse_class(fmclass):
    class_name = fmclass.get("name")
    print(f"Processing class: {class_name}")

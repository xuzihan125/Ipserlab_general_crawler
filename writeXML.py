import xml.etree.ElementTree as ET
import os
# dir to save the file
# dir = "./data"

def writeFile(file_name: str, data: dict, type: str, dir="./data"):
    """

    :param file_name: file name to be stored, should be end in xml
    :param data: data to be saved.
    should be in set, only save the inner dict. Example as following:
    {"data1":{"property1": data1, "property2": data2}}
    :param type: the parent type to be saved:
    <root>
        <type>
            <property1> data1-1 </property1>
            <property2> data1-2 </property2>
        </type>
        <type>
            <property1> data2-1 </property1>
            <property2> data2-2 </property2>
        </type>
    </root>

    """
    if not os.path.exists(dir):
        os.makedirs(dir)
    root = ET.Element("root")
    build_tree(root, data)
    # for key in data.keys():
    #     parrent_item = ET.SubElement(root, type)
    #     for property in data[key].keys():
    #         item = ET.SubElement(parrent_item, property)
    #         item.text = data[key][property]

    tree = ET.ElementTree(root)

    with open(dir+"/" + file_name, "wb") as f:
        tree.write(f)

def build_tree(parent: ET.Element, data: dict):
    """

    :param file_name: file name to be stored, should be end in xml
    :param data: data to be saved.
    should be in set, only save the inner dict. Example as following:
    {"data1":{"property1": data1, "property2": data2}}
    :param type: the parent type to be saved:
    <root>
        <type>
            <property1> data1-1 </property1>
            <property2> data1-2 </property2>
        </type>
        <type>
            <property1> data2-1 </property1>
            <property2> data2-2 </property2>
        </type>
    </root>

    """
    # if not os.path.exists(dir):
    #     os.makedirs(dir)
    # root = ET.Element("root")
    for key, value in data.items():
        parrent_item = ET.SubElement(parent, key)
        if isinstance(value, dict):
            build_tree(parrent_item, value)
        elif isinstance(value, list):
            for item in value:
                parrent_item_list = ET.SubElement(parrent_item, key+"_item")
                build_tree(parrent_item_list, item)
        else:
            parrent_item.text = str(value)
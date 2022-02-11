import xml.etree.ElementTree as ElementTree


def parse_category_name(category_xml_string):
    category_xml = ElementTree.fromstring(category_xml_string)
    category_name = category_xml.find('*').find('name').find('language').text
    # print(category_name)
    return category_name


def parse_category_url(product_details):
    return product_details.find('*').find('id_category_default').get("{http://www.w3.org/1999/xlink}href")


def parse_product_index(product_details):
    return product_details.find('*').find('reference').text


def remove_node(product_details, node_name):
    product_node = product_details.find('*')

    node = product_node.find(node_name)
    product_node.remove(node)

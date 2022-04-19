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


def parse_product_id(product_details):
    return product_details.find('*').find('id').text


def remove_node(product_details, node_name):
    product_node = product_details.find('*')

    node = product_node.find(node_name)
    product_node.remove(node)


def parse_product_price(product_details):
    product_price_text = product_details.find('*').find('price').text
    return float(product_price_text.replace(',', '.'))


def update_price(shop_product_details, price_pln):
    product_node = shop_product_details.find('*')
    # print(product_node.find('price').text)
    product_node.find('price').text = str(price_pln)
    # print(product_node.find('price').text)


def update_is_active(shop_product_details, is_active):
    product_node = shop_product_details.find('*')
    # print(product_node.find('active').text)
    product_node.find('active').text = str(int(is_active is True))
    # print(product_node.find('active').text)


def get_specific_price_element(reduction, from_quantity, product_id, element_id = None):

    # create from xml string
    specific_price_xml = ElementTree.fromstring('<prestashop xmlns:xlink="http://www.w3.org/1999/xlink"><specific_price></specific_price></prestashop>')
    specific_price_node = specific_price_xml.find('specific_price')

    if element_id is not None:
        element = ElementTree.SubElement(specific_price_node, 'id')
        element.text = element_id

    element = ElementTree.SubElement(specific_price_node, 'id_shop')
    element.text = '0'
    element = ElementTree.SubElement(specific_price_node, 'id_cart')
    element.text = '0'
    element = ElementTree.SubElement(specific_price_node, 'id_currency')
    element.text = '0'
    element = ElementTree.SubElement(specific_price_node, 'id_country')
    element.text = '0'
    element = ElementTree.SubElement(specific_price_node, 'id_group')
    element.text = '0'
    element = ElementTree.SubElement(specific_price_node, 'id_customer')
    element.text = '0'
    element = ElementTree.SubElement(specific_price_node, 'id_product')
    element.text = str(product_id)
    element.set('xlink:href', 'https://chrupnazdrowie.pl/api/products/' + str(product_id))

    element = ElementTree.SubElement(specific_price_node, 'price')
    element.text = '-1'
    element = ElementTree.SubElement(specific_price_node, 'from_quantity')
    element.text = str(from_quantity)
    element = ElementTree.SubElement(specific_price_node, 'reduction')
    element.text = str(reduction)
    element = ElementTree.SubElement(specific_price_node, 'reduction_tax')
    element.text = '1'
    element = ElementTree.SubElement(specific_price_node, 'reduction_type')
    element.text = 'percentage'
    element = ElementTree.SubElement(specific_price_node, 'from')
    element.text = '0000-00-00 00:00:00'
    element = ElementTree.SubElement(specific_price_node, 'to')
    element.text = '0000-00-00 00:00:00'

    return specific_price_xml


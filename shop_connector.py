import base64
import logging
import xml.etree.ElementTree as ElementTree

import requests

import xml_util
from constants import SHOP_PRODUCTS_URL, SHOP_API_TOKEN, SHOP_SPECIFIC_PRICES_URL


def make_get_request(url):
    response = requests.get(url, headers=get_headers())

    # logging.info("GET URL: %s, size: %s", url, len(response.text))

    return response.text


def get_product_list():
    product_list_xml_string = make_get_request(SHOP_PRODUCTS_URL)
    return ElementTree.fromstring(product_list_xml_string)[0]


def get_headers():
    encoded = base64.b64encode((SHOP_API_TOKEN + ":").encode())
    token = f"Basic {encoded.decode()}"
    return {"Authorization": token}


def make_put_request(url, payload):
    response = requests.put(url, payload, headers=get_headers())

    # logging.info("PUT URL: %s, RQ size: %s, RS size: %s", url, len(payload.text), len(response.text))

    return response


def make_post_request(url, payload):
    response = requests.post(url, payload, headers=get_headers())

    # logging.info("PUT URL: %s, RQ size: %s, RS size: %s", url, len(payload.text), len(response.text))

    return response


def get_product_details(product_url):
    product_details_xml_string = make_get_request(product_url)
    # print(ET.fromstring(product_details_xml_string)[0])
    return ElementTree.ElementTree(ElementTree.fromstring(product_details_xml_string))


def get_product_specific_prices(product_id):

    product_specific_prices_xml_string = make_get_request(SHOP_SPECIFIC_PRICES_URL + "/?display=full&filter[id_product]=" + product_id)

    print(product_specific_prices_xml_string)

    return ElementTree.ElementTree(ElementTree.fromstring(product_specific_prices_xml_string))


def clear_product_xml_for_saving(product_details):
    xml_util.remove_node(product_details, 'manufacturer_name')
    xml_util.remove_node(product_details, 'quantity')
    return product_details


def update_product(product_url, product_details):
    product_ready_to_save = clear_product_xml_for_saving(product_details)

    xml_to_update = ElementTree.tostring(product_ready_to_save.getroot(), encoding='utf8', method='xml')
    # print(xml_to_update)
    response = make_put_request(product_url, xml_to_update)

    if response.status_code != 200:
        logging.warning("Problem updating product: XML: %s, response: %s", xml_to_update, response.text)


def save_specific_price(xml):
    xml_to_save = ElementTree.tostring(xml, encoding='utf8', method='xml')

    make_post_request(SHOP_SPECIFIC_PRICES_URL, xml_to_save)


def save_new_specific_price(reduction, quantity, product_id):
    xml = xml_util.get_specific_price_element(reduction, quantity, product_id)

    save_specific_price(xml)


def update_specific_price(reduction, quantity, product_id, specific_price_id):
    url = SHOP_SPECIFIC_PRICES_URL + "/" + specific_price_id
    xml = xml_util.get_specific_price_element(reduction, quantity, product_id, specific_price_id)
    xml_to_update = ElementTree.tostring(xml, encoding='utf8', method='xml')

    make_put_request(url, xml_to_update)

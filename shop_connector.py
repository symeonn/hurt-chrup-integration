import base64
import logging
import xml.etree.ElementTree as ElementTree

import requests

import xml_util
from constants import SHOP_PRODUCTS_URL, SHOP_API_TOKEN


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


def get_product_details(product_url):
    product_details_xml_string = make_get_request(product_url)
    # print(ET.fromstring(product_details_xml_string)[0])
    return ElementTree.ElementTree(ElementTree.fromstring(product_details_xml_string))


def clear_product_xml_for_saving(product_details):
    xml_util.remove_node(product_details, 'manufacturer_name')
    xml_util.remove_node(product_details, 'quantity')
    return product_details


def save_product(product_url, product_details):
    product_ready_to_save = clear_product_xml_for_saving(product_details)

    xml_to_update = ElementTree.tostring(product_ready_to_save.getroot(), encoding='utf8', method='xml')
    # print(xml_to_update)
    response = make_put_request(product_url, xml_to_update)

    if response.status_code != 200:
        logging.warning("Problem updating product: XML: %s, response: %s", xml_to_update, response.text)

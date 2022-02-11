import xml.etree.ElementTree as ElementTree
import requests
import base64
import xml_util
from constants import SHOP_PRODUCTS_URL, SHOP_API_TOKEN


def make_get_request(url):
    response = requests.get(url, headers=get_headers())
    # print(response.text)
    return response.text


def get_product_list():
    product_list_xml_string = make_get_request(SHOP_PRODUCTS_URL)
    return ElementTree.fromstring(product_list_xml_string)[0]


# tmpFilename = "productList.xml"


def get_headers():
    encoded = base64.b64encode((SHOP_API_TOKEN + ":").encode())
    token = f"Basic {encoded.decode()}"
    return {"Authorization": token}


def make_put_request(url, payload):
    response = requests.put(url, payload, headers=get_headers())
    # print(response.text)
    return response.text


def get_product_details(product_url):
    # print(productUrl)
    product_details_xml_string = make_get_request(product_url)
    # print(product_details_xml_string)
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
    print(response)

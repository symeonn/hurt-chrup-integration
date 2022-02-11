import shop_connector
from constants import SHOP_PRODUCTS_URL
import xml_util


def process_products():
    for product in shop_connector.get_product_list():
        # print(elem)
        product_id = product.attrib['id']
        product_url = product.get("{http://www.w3.org/1999/xlink}href")
        print(f"Id: {product_id}, URL: {product_url}")
        # process_product(product_url)


def process_product(product_url):
    product_details = shop_connector.get_product_details(product_url)

    if product_to_process(product_details):

        
        product_details = update_product_details(product_details)
        shop_connector.save_product(product_url, product_details)
    else:
        return


def product_to_process(product_details):
    return index_to_process(product_details) and category_to_process(product_details)


def index_to_process(product_details):
    index = xml_util.parse_product_index(product_details)
    # print(index is not None and index.isnumeric())
    return index is not None and index.isnumeric()


def category_to_process(product_details):
    category_url = xml_util.parse_category_url(product_details)
    # print("imp" != getCategoryName(category_url))
    return "imp" != get_category_name(category_url)


def get_category_name(category_url):
    category_xml_string = shop_connector.make_get_request(category_url)
    category_name = xml_util.parse_category_name(category_xml_string)
    return category_name


def update_product_details(product_details):
    product_node = product_details.find('*')
    print(product_node.find('name').find('language').text)
    product_details.find('*').find('name').find('language').text = "nowy name 6"
    print(product_node.find('name').find('language').text)
    return product_details

import logging
import multiprocessing
from itertools import repeat

import product_updater
import shop_connector
import xml_util

logger = logging.getLogger(__name__)


def process_products(hurt_all_products):
    a_pool = multiprocessing.Pool()
    logger.info('Number of processes: %s', a_pool._processes)

    a_pool.starmap(process, zip(shop_connector.get_product_list(), repeat(hurt_all_products)))


def process(product, hurt_all_products):
    product_id = product.attrib['id']
    print(product_id, end=',')

    product_url = product.get("{http://www.w3.org/1999/xlink}href")
    # print(f"Id: {product_id}, URL: {product_url}")

    process_product(product_url, hurt_all_products)


def get_hurt_product(shop_product_details, hurt_all_products):
    product_index = xml_util.parse_product_index(shop_product_details)
    hurt_product_by_index = hurt_all_products[hurt_all_products['Indeks'].isin([product_index])]
    return hurt_product_by_index


def process_product(product_url, hurt_all_products):
    shop_product_details = shop_connector.get_product_details(product_url)

    if product_to_process(shop_product_details, hurt_all_products):

        hurt_product = get_hurt_product(shop_product_details, hurt_all_products)
        shop_product_details = update_product_details(shop_product_details, hurt_product)
        shop_connector.save_product(product_url, shop_product_details)
        return
    else:
        return


def shop_product_in_hurt(product_details, hurt_all_products):
    shop_product_exists_in_hurt = xml_util.parse_product_index(product_details) in hurt_all_products.Indeks.values
    return shop_product_exists_in_hurt


def product_to_process(product_details, hurt_all_products):
    return index_to_process(product_details) \
           and category_to_process(product_details) \
           and shop_product_in_hurt(product_details, hurt_all_products)


def index_to_process(product_details):
    index = xml_util.parse_product_index(product_details)
    return index is not None and index.isnumeric()


def category_to_process(product_details):
    category_url = xml_util.parse_category_url(product_details)
    return "imp" != get_category_name(category_url)


def get_category_name(category_url):
    category_xml_string = shop_connector.make_get_request(category_url)
    category_name = xml_util.parse_category_name(category_xml_string)
    return category_name


def update_product_details(shop_product_details, hurt_product):
    price_pln = product_updater.calculate_new_price(hurt_product)
    is_product_active = product_updater.get_product_active(hurt_product)
    # multi_item = product_updater.get_multi_items(hurt_product)

    # need to POST new specific_prices with from_quantity and reduction and id_product and price -1 and reduction_type
    # xml_util.
    logger.info("Update: Indeks: %s, Old price: %s, New price: %s, Is active: %s ",
                xml_util.parse_product_index(shop_product_details),
                xml_util.parse_product_price(shop_product_details),
                price_pln,
                is_product_active)

    xml_util.update_price(shop_product_details, price_pln)
    xml_util.update_is_active(shop_product_details, is_product_active)

    return shop_product_details

import logging
import multiprocessing
from itertools import repeat

import hurt_product_util
import product_updater
import shop_connector
import xml_util

logger = logging.getLogger(__name__)


def process_products(hurt_all_products):
    a_pool = multiprocessing.Pool()
    logger.info('Number of processes: %s', a_pool._processes)
    shop_all_products = shop_connector.get_product_list()
    return a_pool.starmap(process, zip(shop_all_products, repeat(hurt_all_products)))

    # for shop_product in shop_all_products:
    #     process(shop_product, hurt_all_products)


def process(shop_product, hurt_all_products):
    product_id = shop_product.attrib['id']
    print(product_id, end=',')

    product_url = shop_product.get("{http://www.w3.org/1999/xlink}href")
    # print(f"Id: {product_id}, URL: {product_url}")

    return process_product(product_url, hurt_all_products)


def get_hurt_product(shop_product_details, hurt_all_products):
    product_index = xml_util.parse_product_index(shop_product_details)
    hurt_product_by_index = hurt_all_products[hurt_all_products['Indeks'].isin([product_index])]
    return hurt_product_by_index


def remove_product(product_list, product_to_remove):
    product_index = xml_util.parse_product_index(product_to_remove)

    return product_list.drop(product_list.index[product_list['Indeks'] == product_index])


def process_product(shop_product_url, hurt_all_products):
    shop_product_details = shop_connector.get_product_details(shop_product_url)

    if product_to_process(shop_product_details, hurt_all_products):

        if not is_category_import(shop_product_details):
            hurt_product = get_hurt_product(shop_product_details, hurt_all_products)
            shop_product_details = update_product_details(shop_product_details, hurt_product)
            shop_connector.save_product(shop_product_url, shop_product_details)

        # hurt_all_products = remove_product(hurt_all_products, shop_product_details)

        return xml_util.parse_product_index(shop_product_details)

    else:
        return -1


def shop_product_in_hurt(product_details, hurt_all_products):
    shop_product_exists_in_hurt = xml_util.parse_product_index(product_details) in hurt_all_products.Indeks.values
    return shop_product_exists_in_hurt


def product_to_process(product_details, hurt_all_products):
    return index_to_process(product_details) and shop_product_in_hurt(product_details, hurt_all_products)


def index_to_process(product_details):
    index = xml_util.parse_product_index(product_details)
    return index is not None and index.isnumeric()


def is_category_import(product_details):
    category_url = xml_util.parse_category_url(product_details)
    return category_url.endswith("/118")


def update_product_details(shop_product_details, hurt_product):
    new_price_pln = product_updater.calculate_new_price(hurt_product)
    is_product_active = product_updater.get_product_active(hurt_product)
    quantity = hurt_product_util.get_product_quantity(hurt_product)
    multi_item_price = product_updater.get_multi_items_price(hurt_product)
    # get all s_p for product with specific_prices?display=full&filter[id_product]=1137
    # remove all specific_prices for this product
    # need to POST new specific_prices with from_quantity [quantity] and reduction [0.1 (10%)] and id_product and price [-1] and reduction_type [percentage]
    # do I need to post new s_p when price is changed or only when quantity is changed?
    # I can update (and even should) s_p for product

    logger.info("Update: Indeks: %s, Old price: %s, New price: %s, Active: %s, Quantity: %s, Multi price: %s",
                xml_util.parse_product_index(shop_product_details),
                round(xml_util.parse_product_price(shop_product_details), 2),
                new_price_pln,
                is_product_active,
                quantity,
                multi_item_price)

    xml_util.update_price(shop_product_details, new_price_pln)
    xml_util.update_is_active(shop_product_details, is_product_active)
    # xml_util.update_multi_items(shop_product_details, multi_item)

    return shop_product_details

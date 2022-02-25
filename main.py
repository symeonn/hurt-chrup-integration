import logging
import os
import sys

from hurt_processor import fetch_hurt_data
from product_processor import process_products
from product_updater import fetch_euro_currency

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s [%(filename)s:%(lineno)s ] %(levelname)s: %(message)s"
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'logs', 'main.log')

logging.basicConfig(filename=LOG_FILE_PATH, format=FORMAT, encoding='utf-8', level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))  # comment to log to file, uncomment to log to console


def init_application():
    fetch_euro_currency()


def main():
    init_application()
    logger.info('======================Start sync======================')

    hurt_all_products = fetch_hurt_data()
    process_products(hurt_all_products)

    # test_product_url = SHOP_PRODUCTS_URL + "/1137"

    # test_product_url = SHOP_PRODUCTS_URL + "/9604"  # indeks 719086
    # test_product_url = SHOP_PRODUCTS_URL + "/866"  # indeks 13113315
    # test_product_url = SHOP_PRODUCTS_URL + "/92"  # indeks 117127
    # process_product(test_product_url, hurt_all_products)

    logger.info('\n======================End sync======================')


if __name__ == "__main__":
    main()

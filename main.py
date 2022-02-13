import os
import sys

from constants import SHOP_PRODUCTS_URL, LOCAL_FILE_PATH
from hurt_processor import fetch_hurt_data
from product_processor import process_products, process_product
from product_updater import fetch_euro_currency


def main():
    # print(sys.path[0])
    fetch_euro_currency()
    hurt_all_products = fetch_hurt_data()

    # process_products(hurt_all_products)




    # test_product_url = SHOP_PRODUCTS_URL + "/1137"

    test_product_url = SHOP_PRODUCTS_URL + "/9604" # indeks 719086
    process_product(test_product_url, hurt_all_products)


if __name__ == "__main__":
    main()

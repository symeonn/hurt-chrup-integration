import os
import sys

from constants import SHOP_PRODUCTS_URL, LOCAL_FILE_PATH
from hurt_processor import fetch_hurt_data
from product_processor import process_products, process_product


def main():
    print("Hello World!")
    # print(sys.path[0])
    fetch_hurt_data()

    # process_products()
    # test_product_url = SHOP_PRODUCTS_URL + "/1137"
    # process_product(test_product_url)


if __name__ == "__main__":
    main()

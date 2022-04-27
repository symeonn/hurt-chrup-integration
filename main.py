import datetime
import logging
import os
import sys

from constants import LOCAL_FILE_PATH
from hurt_processor import fetch_hurt_data
from product_processor import process_products
from product_updater import fetch_euro_currency

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s %(levelname)s: %(message)s"
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'logs', 'main.log')

logging.basicConfig(filename=LOG_FILE_PATH, format=FORMAT, encoding='utf-8', level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))  # comment to log to file, uncomment to log to console


def main():
    euro_pln_rate = fetch_euro_currency()

    logger.info('======================Start sync======================')
    start_time = datetime.datetime.now()
    logger.info('Started at: ' + str(start_time))

    hurt_all_products = fetch_hurt_data()
    indexes_processed = process_products(hurt_all_products)
    # print(f"Indekses processed: {indexes_processed}")

    new_products_to_csv(hurt_all_products, indexes_processed)

    logger.info('\n======================End sync======================')
    end_time = datetime.datetime.now()
    logger.info('Finished at: ' + str(end_time))
    logger.info('Time elapsed: ' + str(end_time - start_time))
    logger.info('Euro price: %s', euro_pln_rate)


def new_products_to_csv(hurt_all_products, indexes_processed):
    hurt_new_products = hurt_all_products.drop(hurt_all_products.index[hurt_all_products['Indeks'].isin(indexes_processed)])
    # hurt_new_products['NamePL'] = hurt_new_products['Name'].apply(translate_de_to_pl)
    hurt_new_products.to_csv(os.path.join(sys.path[0], LOCAL_FILE_PATH, 'hurt_new.csv'))


if __name__ == "__main__":
    main()

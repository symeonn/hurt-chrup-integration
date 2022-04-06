import logging
import os
import sys

import pandas

import hurt_connector
from constants import FRUITS_AND_VEGES_FILENAME, LOCAL_FILE_PATH, FRESH_FILENAME, FOOD_FILENAME

logger = logging.getLogger(__name__)

columns_to_import = [0, 1, 6, 22, 37, 60, 65]
columns_to_import_names = ['Indeks', 'Change', 'Name', 'Quantity', 'Price', 'ItemType', 'Unit']


def get_data_from_file(filename):
    hurt_connector.fetch_file_from_hurt_ftp(filename)
    return get_df_from_csv(filename)


def get_df_from_csv(filename):
    df = pandas.read_csv(os.path.join(sys.path[0], LOCAL_FILE_PATH, filename), sep=';', encoding='CP850', skiprows=[0],
                         header=None, usecols=columns_to_import, names=columns_to_import_names, dtype={'Indeks': 'str'})
    # print(f"File: {os.path.join(sys.path[0], LOCAL_FILE_PATH, filename)}, original lines: {len(df.index)}")
    return df


def filter_indeks_digit_only(df):
    return df[df['Indeks'].astype(str).str.isdigit()]


def fetch_hurt_data():
    vege_hurt_cleared = filter_indeks_digit_only(get_data_from_file(FRUITS_AND_VEGES_FILENAME))
    logger.info('File: %s, Shop lines: %s', FRUITS_AND_VEGES_FILENAME, len(vege_hurt_cleared.index))

    fresh_hurt_cleared = filter_indeks_digit_only(get_data_from_file(FRESH_FILENAME))
    logger.info('File: %s, Shop lines: %s', FRESH_FILENAME, len(fresh_hurt_cleared.index))

    food_hurt_cleared = filter_indeks_digit_only(get_data_from_file(FOOD_FILENAME))
    logger.info('File: %s, Shop lines: %s', FOOD_FILENAME, len(food_hurt_cleared.index))

    products_from_hurt = pandas.concat([vege_hurt_cleared, fresh_hurt_cleared, food_hurt_cleared])

    # print(products_from_hurt)

    return products_from_hurt

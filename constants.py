from configparser import ConfigParser

parser = ConfigParser()
_ = parser.read('notebook.cfg')

LOCAL_FILE_PATH = parser['general']['LOCAL_FILE_PATH']

HURT_HOSTNAME = parser['hurt']['HURT_HOSTNAME']
HURT_USERNAME = parser['hurt']['HURT_USERNAME']
HURT_PASSWORD = parser['hurt']['HURT_PASSWORD']
FRUITS_AND_VEGES_FILENAME = parser['hurt']['FRUITS_AND_VEGES_FILENAME']
FRESH_FILENAME = parser['hurt']['FRESH_FILENAME']
FOOD_FILENAME = parser['hurt']['FOOD_FILENAME']

SHOP_API_TOKEN = parser['shop']['SHOP_API_TOKEN']
SHOP_PRODUCTS_URL = parser['shop']['SHOP_PRODUCTS_URL']

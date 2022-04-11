from forex_python.converter import CurrencyRates
import logging
import hurt_product_util

logger = logging.getLogger(__name__)

price_with_margin = 1.8
euro_pln_rate = None
discount = 0.1
price_with_discount = 1-discount


def fetch_euro_currency():
    logger.info("fetching euro/pln rate...")
    currency_rates = CurrencyRates()
    global euro_pln_rate
    euro_pln_rate = currency_rates.get_rate('EUR', 'PLN')
    logger.info('Euro price: %s', euro_pln_rate)
    # df['PricePLN'] = (df['Price'].apply(convertToFloat)*price_with_margin*euroPlnRate).apply(lambda x : format(x, '.2f'))
    return euro_pln_rate


def calculate_new_price(hurt_product):
    if euro_pln_rate is None:
        fetch_euro_currency()

    hurt_price_eur = hurt_product_util.get_product_price(hurt_product)
    new_price_pln = hurt_price_eur * price_with_margin * euro_pln_rate
    # logger.info("Price in EUR: %s, price in PLN: %s", hurt_price_eur, new_price_pln)
    return round(new_price_pln, 2)


def get_product_active(hurt_product):
    is_active = hurt_product.Change.iloc[0] in ['N', 'A', 'W']
    # print(f"Product active?: {is_active}")
    return is_active


def get_multi_items_price(hurt_product):

    # dla produktów gdzie trzeba wziąć z hurtowni opakowanie zbiorcze
    # zrobić dla klienta w sklepie rabat kiedy zamówi ilość sztuk tyle co w opakowaniu zbiorczym
    # Przykład:
    #   zamawiamy z hurtowni jogurty o pakowaniu zbiorczym jest 6 sztuk po np. 2eur/szt
    #   dla klienta sztuka będzie wyliczona czyli jakieś 12zł
    #   a jak weźmie całe opakowanie czyli 6 szt to będzie np rabat 10% czyli cena 6x12zł*10% = 64,8zł
    quantity = hurt_product_util.get_product_quantity(hurt_product)

    if quantity > 1:
        # print(f"Ilość: {quantity}")

        multi_item_price = calculate_new_price(hurt_product) * quantity * price_with_discount
        # print(multi_item_price)
        return round(multi_item_price, 2)

    return None

from forex_python.converter import CurrencyRates

price_with_margin = 1.5
euro_pln_rate = None


def fetch_euro_currency():
    print("fetching euro/pln rate...")
    currency_rates = CurrencyRates()
    global euro_pln_rate
    euro_pln_rate = currency_rates.get_rate('EUR', 'PLN')
    print(f"Euro price: {euro_pln_rate}")
    # df['PricePLN'] = (df['Price'].apply(convertToFloat)*price_with_margin*euroPlnRate).apply(lambda x : format(x, '.2f'))
    return euro_pln_rate


def calculate_new_price(hurt_price_eur):
    if euro_pln_rate is None:
        fetch_euro_currency()

    new_price_pln = float(hurt_price_eur.replace(',', '.')) * price_with_margin * euro_pln_rate
    print(f"Price in EUR: {hurt_price_eur}, price in PLN: {new_price_pln}")

    return format(new_price_pln, '.2f')


def get_product_active():
    return False


def get_multi_items():
    return 0

def get_product_price(hurt_product):
    hurt_product_price_string = hurt_product.Price.iloc[0]
    hurt_product_price = float(hurt_product_price_string.replace(',', '.'))
    # print(f"Product price EUR: {hurt_product_price}")
    return hurt_product_price


def get_product_quantity(hurt_product):
    quantity_string = hurt_product.Quantity.iloc[0]
    quantity = float(quantity_string.replace(',', '.'))
    # print(f"Quantity: {quantity}")
    return quantity

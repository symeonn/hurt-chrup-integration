import os
import sys

from constants import FRUITS_AND_VEGES_FILENAME, LOCAL_FILE_PATH, FRESH_FILENAME, FOOD_FILENAME
import hurt_connector
import pandas

columns_to_import = [0, 1, 6, 22, 37, 60, 65]
columns_to_import_names = ['Indeks', 'Change', 'Name', 'Quantity', 'Price', 'ItemType', 'Unit']


def get_data_from_file(filename):
    # datesOld = getDatesFromCSV(filename)
    # print(datesOld)
    hurt_connector.fetch_file_from_hurt_ftp(filename)
    # datesNew = getDatesFromCSV(filename)

    # print(datesNew)
    return get_df_from_csv(filename)


def get_df_from_csv(filename):
    df = pandas.read_csv(os.path.join(sys.path[0], LOCAL_FILE_PATH, filename), sep=';', encoding='CP850', skiprows=[0], header=None, usecols=columns_to_import, names=columns_to_import_names, dtype={'Indeks': 'str'})
    # print(f"File: {os.path.join(sys.path[0], LOCAL_FILE_PATH, filename)}, original lines: {len(df.index)}")
    return df


def filter_indeks_digit_only(df):
    return df[df['Indeks'].astype(str).str.isdigit()]


def fetch_hurt_data():

    vege_hurt_cleared = filter_indeks_digit_only(get_data_from_file(FRUITS_AND_VEGES_FILENAME))
    # vegeBnnShop = filterInByIndeks(vege_hurt_cleared, shopIndeksNoNullCleared)
    print(f"File: {FRUITS_AND_VEGES_FILENAME}, Shop lines: {len(vege_hurt_cleared.index)}")

    fresh_hurt_cleared = filter_indeks_digit_only(get_data_from_file(FRESH_FILENAME))
    # freshBnnShop = filterInByIndeks(fresh_hurt_cleared, shopIndeksNoNullCleared)
    print(f"File: {FRESH_FILENAME}, Shop lines: {len(fresh_hurt_cleared.index)}")

    food_hurt_cleared = filter_indeks_digit_only(get_data_from_file(FOOD_FILENAME))
    # dryBnnShop = filterInByIndeks(food_hurt_cleared, shopIndeksNoNullCleared)
    print(f"File: {FOOD_FILENAME}, Shop lines: {len(food_hurt_cleared.index)}")

    # print(dryBnn)

    products_from_hurt = pandas.concat([vege_hurt_cleared, fresh_hurt_cleared, food_hurt_cleared])

    # print(products_from_hurt)

    return products_from_hurt

    # addTotalPriceColumn(allProducts)
    # addShowColumn(products_from_shop_in_hurt)
    #
    # addPricePLNColumn(products_from_shop_in_hurt)
    # shopProductsToUpdate = shopProductsWithClearedIndex.merge(products_from_shop_in_hurt[['Indeks', 'Show', 'PricePLN']],
    #                                                           on=['Indeks'], how='left')
    # shopProductsToUpdate['Show'] = shopProductsToUpdate['Show'].fillna(0)
    # shopProductsToUpdate['Show'] = shopProductsToUpdate['Show'].astype(int)
    #
    # outputFilename = "update.csv"
    # outputFilenameWithTimestamp = getTimestamp() + outputFilename
    # print(f"Update filename: {outputFilenameWithTimestamp}")
    # pd.DataFrame.to_csv(shopProductsToUpdate, outputFilenameWithTimestamp, sep=';', na_rep='.', index=False)
    #
    # uploadFiletoFtp(outputFilenameWithTimestamp)
    #
    # print(shopProductsToUpdate[shopProductsToUpdate['Show'].eq(0)])
    # print(products_from_shop_in_hurt[~products_from_shop_in_hurt['Change'].isin(["A"])])
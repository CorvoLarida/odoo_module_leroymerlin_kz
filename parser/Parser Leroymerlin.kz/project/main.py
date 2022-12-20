from project.get_all_urls import get_all_urls
from project.one_product_data import parsingData


def main():
    # get_all_urls.get_all_product_urls()
    # get_all_urls.write_product_urls_to_txt()
    # parsingData.get_all_products_data_from_txt()
    parsingData.get_some_products_data_from_txt('all_products', 30)
    # parsingData.get_one_product_data_from_txt('out_of_stock')


if __name__ == '__main__':
    main()

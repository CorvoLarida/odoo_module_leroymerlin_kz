import datetime
import random
import time

import requests
from bs4 import BeautifulSoup
import csv


class DataParser:
    num_of_iterations = 0
    right_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    def __init__(self, url):
        self.all_data = []
        self.special_order = None
        self.description = None
        self.quantity = None
        self.price = None
        self.name = None
        self.categoriesList = None
        self.valuesList = None
        self.detailsList = None
        self.productId = None
        self.url = url

    def fromNetToLocal(self):
        headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

        req = requests.get(self.url, headers=headers)
        src = req.text
        # self.local_html = self.url[::-1][2:10][::-1] + '.html'
        print(self.url)
        with open('one_product_data/last_product.html', "w", encoding="utf-8") as file:
            file.write(src)

    def details(self):
        with open('one_product_data/last_product.html', encoding="utf-8") as file:
            source = file.read()

        soup = BeautifulSoup(source, "lxml")
        tds = soup.findAll("td")
        cleantds = []

        for td in tds:
            td = td.text.strip()
            if len(td) > 1:
                td = td.replace(":", "")
            cleantds.append(td)

        try:
            self.detailsList = cleantds[::2]
        except Exception as ex:
            self.detailsList = 'NO DATA'

        try:
            self.valuesList = cleantds[1::2]
        except Exception as ex:
            self.valuesList = 'NO DATA'

        try:
            self.productId = self.valuesList[0]
        except Exception as ex:
            self.productId = 'NO DATA'

        self.all_data.append(self.detailsList)
        self.all_data.append(self.valuesList)
        self.all_data.append(self.productId)

    def catalog(self):
        with open('one_product_data/last_product.html', encoding="utf-8") as file:
            source = file.read()

        soup = BeautifulSoup(source, "lxml")
        categories = soup.findAll(class_="breadcrumbs__link")
        self.categoriesList = []
        try:
            for category in categories:
                category = category.text.strip()
                self.categoriesList.append(category)
            self.categoriesList.pop(0)
            self.categoriesList.pop(0)
        except Exception as ex:
            self.categoriesList = 'NO DATA'
        self.all_data.append(self.categoriesList)

    def product(self):
        with open('one_product_data/last_product.html', encoding="utf-8") as file:
            source = file.read()

        soup = BeautifulSoup(source, "lxml")

        try:
            self.name = soup.find(class_="product__h1-mobile").text.strip()
        except Exception as ex:
            self.name = 'NO DATA'
        print('Name: ' + self.name)

        try:
            self.price = soup.find(class_="product__price").next_element.text.strip().replace(" ", "")
        except Exception as ex:
            self.price = 'NO DATA'
        print('Price: ' + self.price)

        try:
            self.quantity = soup.find("div", class_="product__row").find('vue-catalogue-detail-spinner').get('max-value')
        except Exception as ex:
            self.quantity = 'NO DATA'
        print('Quantity: ' + self.quantity)

        descriptions_p = soup.find('div', class_='about__descr__text').findAll('p')
        self.description = ''
        try:
            for desc in descriptions_p:
                if "СКАЧАТЬ" in desc.text:
                    pass
                else:
                    self.description += desc.text
            if self.description == "":
                self.description = "НЕТ ОПИСАНИЯ"
        except Exception as ex:
            self.description = 'NO DATA'
        print('Description: ' + self.description)

        try:
            self.special_order = soup.find('p', class_='product__delivery-title')
            if self.special_order is None:
                self.special_order = False
            else:
                self.special_order = True
        except Exception as ex:
            self.special_order = 'NO DATA'
        print('Is Special Order: ' + str(self.special_order))

        self.all_data.append(self.name)
        self.all_data.append(self.price)
        self.all_data.append(self.quantity)
        self.all_data.append(self.description)
        self.all_data.append(self.special_order)

    def write_data_to_csv(self):

        def write_details():
            headers_details = ['productnumber', 'detail', 'value']
            with open(f"final/{DataParser.right_now}_for_table_details.csv", "a", encoding="utf-8",
                      newline='') as details_csv:
                writer = csv.DictWriter(details_csv, fieldnames=headers_details, delimiter='\t')
                if DataParser.num_of_iterations < 1:
                    writer.writeheader()
                for i in range(0, len(self.detailsList)):
                    writer.writerow(
                        {'productnumber': self.productId, 'detail': self.detailsList[i], 'value': self.valuesList[i]}
                    )

        def write_catalog():
            headers_catalog = ['productnumber', 'categorylv1', 'categorylv2', 'categorylv3']
            with open(f"final/{DataParser.right_now}_for_table_catalog.csv", "a", encoding="utf-8",
                      newline='') as catalog_csv:
                writer = csv.DictWriter(catalog_csv, fieldnames=headers_catalog, delimiter='\t')
                if DataParser.num_of_iterations < 1:
                    writer.writeheader()
                writer.writerow(
                    {'productnumber': self.productId, 'categorylv1': self.categoriesList[0],
                     'categorylv2': self.categoriesList[1], 'categorylv3': self.categoriesList[2]}
                )

        def write_product():
            headers_products = ['productnumber', 'name', 'price', 'quantity', 'description', 'specialorder']
            with open(f"final/{DataParser.right_now}_for_table_products.csv", "a", encoding="utf-8",
                      newline='') as product_csv:
                writer = csv.DictWriter(product_csv, fieldnames=headers_products, delimiter='\t')
                if DataParser.num_of_iterations < 1:
                    writer.writeheader()
                writer.writerow(
                    {'productnumber': self.productId, 'name': self.name, 'price': self.price,
                     'quantity': self.quantity, 'description': self.description, 'specialorder': self.special_order}
                )

        if 'NO DATA' in self.all_data:
            print("Недостаточно данных")
            with open(f'one_product_data/{DataParser.right_now}_out_of_stock.txt', 'w', encoding='utf-8') as file:
                file.write(self.url)
        else:
            write_details()
            write_catalog()
            write_product()

    def main(self):
        self.fromNetToLocal()
        self.details()
        self.catalog()
        self.product()
        self.write_data_to_csv()
        DataParser.num_of_iterations += 1
        print('#' * 20 + ' end of url parsing')


def get_all_products_data_from_txt():
    with open(f'one_product_data/all_products.txt', encoding='utf-8') as file:
        urls = file.readlines()
    count = 1
    for url in urls:
        print('#' * 10 + '' + str(count) + ' out of ' + str(len(urls)))
        count += 1
        time.sleep(random.randrange(1, 3))
        correct_url = url.rstrip("\n")
        parse = DataParser(correct_url)
        parse.main()


def get_some_products_data_from_txt(name_of_txt_file, num_of_lines):

    with open(f'one_product_data/{name_of_txt_file}.txt', encoding='utf-8') as file:
        not_parsed_urls = file.readlines()

    with open(f'one_product_data/{DataParser.right_now}_some_products.txt', 'w', encoding='utf-8', newline='') as file:
        count = 0
        for url in not_parsed_urls:
            count += 1
            url = random.choice(not_parsed_urls)
            if count > num_of_lines:
                break
            else:
                print(url)
                file.write(url)

    with open(f'one_product_data/{DataParser.right_now}_some_products.txt', encoding='utf-8') as file:
        some_urls = file.readlines()
        no_dup_list = []
        num_of_duplicates = 0
        dup_list = []
        count = 1
        for some_url in some_urls:
            if some_url not in no_dup_list:
                no_dup_list.append(some_url)
            else:
                print("GOT A DUPLICAT")
                num_of_duplicates += 1
                dup_list.append(some_url)
        for no_dup_url in no_dup_list:
            print('#'*10 + '' + str(count) + ' out of ' + str(len(no_dup_list)))
            count += 1
            time.sleep(random.randrange(1, 3))
            correct_url = no_dup_url.rstrip("\n")
            parse = DataParser(correct_url)
            parse.main()
            not_parsed_urls.remove(no_dup_url)
        print('Total Number Of Duplicates: ' + str(num_of_duplicates))
        print('Total Number of Parsed URLs: ' + str(num_of_lines-num_of_duplicates))

    with open(f'one_product_data/{DataParser.right_now}_some_products.txt', 'w', encoding='utf-8') as file:
        for line in no_dup_list:
            file.write(line)

    with open(f'one_product_data/{DataParser.right_now}_not_parsed_products.txt', 'w', encoding='utf-8') as file:
        for left_line in not_parsed_urls:
            file.write(left_line)


def get_one_product_data_from_txt(name_of_txt_file):
    with open(f'one_product_data/{name_of_txt_file}.txt', encoding='utf-8') as file:
        urls = file.readlines()

    url = random.choice(urls).rstrip("\n")
    parse = DataParser(url)
    parse.main()

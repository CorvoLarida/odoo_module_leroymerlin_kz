import datetime
import random
import time

import requests
from bs4 import BeautifulSoup
import json

right_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
lv1list = []
lv1count = 0
lv2list = []
lv2count = 0
lv1_lv2_lists = []
lv1_lv2_count = 0
lv3list = []
lv3count = 0
all_urls = []


def lv1_lv2_get_categories(url):
    headers = {
        'accept': '* / *',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    req = requests.get(url, headers=headers)
    src = req.text

    with open('get_all_urls/extra_html/for_lv1_lv2_categories.html', "w", encoding="utf-8") as file:
        file.write(src)

    with open('get_all_urls/extra_html/for_lv1_lv2_categories.html', encoding="utf-8") as file:
        source = file.read()

    soup = BeautifulSoup(source, 'lxml')

    lv1_lv2_categories = soup.findAll('a', class_="category-list__link")
    for category in lv1_lv2_categories:
        lv1_lv2_lists.append('https://leroymerlin.kz' + category.get('href'))
        global lv1_lv2_count
        print(f'{lv1_lv2_count}_add to lv 1 + 2 list')
        lv1_lv2_count += 1

    def lv1_get_categories():
        lv1categories = soup.findAll('div', class_='subcategory__head-wrapper')
        for category in lv1categories:
            lv1list.append('https://leroymerlin.kz' + category.find('a').get('href'))
            global lv1count
            print(f'{lv1count}_add to lv 1 list')
            lv1count += 1

    lv1_get_categories()


def lv3_get_categories(url):
    headers = {
        'accept': '* / *',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    req = requests.get(url, headers=headers)
    src = req.text

    with open('get_all_urls/extra_html/for_lv3_categories.html', "w", encoding="utf-8") as file:
        file.write(src)

    with open('get_all_urls/extra_html/for_lv3_categories.html', encoding="utf-8") as file:
        source = file.read()

    soup = BeautifulSoup(source, 'lxml')

    lv2categories = soup.findAll('ul', class_='category-list category-list_subcategory js-category-list')
    for lv2 in lv2categories:
        lv3categories = lv2.findAll('a', class_='category-list__link')
        for lv3 in lv3categories:
            global lv3count
            lv3list.append('https://leroymerlin.kz' + lv3.get('href'))
            print(f'{lv3count}_add to lv 3 list')
            lv3count += 1


def get_urls(url):
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept - encoding": "gzip, deflate, br",
        "accept - language": "en; q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "x-language-id": "ru",
        "x-requested-with": "XMLHttpRequest"
    }

    req = requests.get(url=url, headers=headers)

    with open('get_all_urls/extra_html/all_lv3_urls_from_json.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    with open('get_all_urls/extra_html/all_lv3_urls_from_json.html', encoding="utf-8") as file:
        source = file.read()

    soup = BeautifulSoup(source, 'lxml')
    vue_main_menu = soup.find('vue-main-menu').get(':menu-values')
    convert_vue = json.loads(vue_main_menu)

    with open('get_all_urls/extra_json/for_keys_+_lv3_urls.json', 'w', encoding='utf-8') as file:
        json.dump(convert_vue, file, indent=4, ensure_ascii=False)

    with open('get_all_urls/extra_json/for_keys_+_lv3_urls.json', encoding='utf-8') as file:
        doto = json.load(file)

    sub_list1 = doto['2']
    sub_list2 = doto['3']
    big_list = sub_list1 + sub_list2

    urls = []
    numbers = []

    for mini_list in big_list:
        numbers.append(mini_list[0])
        urls.append(mini_list[1])

    all_lvls_dict = {}
    for i in range(0, len(big_list)):
        all_lvls_dict[numbers[i]] = urls[i]

    keys_to_remove = []
    for key, value in all_lvls_dict.items():
        if "https://leroymerlin.kz/" in value:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        all_lvls_dict.pop(key)

    lv3_dict = {key: "https://leroymerlin.kz" + value for key, value in all_lvls_dict.items()}

    keys_to_remove = []
    for key, value in lv3_dict.items():
        if value in lv1_lv2_lists:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        lv3_dict.pop(key)

    def check_for_all_lv3():
        yes_no = []
        for value in lv3list:
            if value in lv3_dict.values():
                yes_no.append(True)
            else:
                yes_no.append(False)

        if False not in yes_no:
            print("Все ссылки собраны")
        else:
            print("Не все ссылки собраны")

    # Откоментировать нижнюю строчку для проверки собранных категорий 3-го уровня
    # check_for_all_lv3()

    def fetch(url, params):
        headers = params['headers']
        body = params['body']
        return requests.post(url, headers=headers, data=body)

    # словарь для проверки
    dict_exmpl = {
        '622': 'https://leroymerlin.kz/catalogue/elektricheskie-shchity-i-miniboksy/',
        '632': 'https://leroymerlin.kz/catalogue/dvoyniki-i-troyniki-dlya-rozetki/',
        '639': 'https://leroymerlin.kz/catalogue/trubki-dlya-domofona/'
    }
    count = 0

    for key, value in dict_exmpl.items():
    # for key, value in lv3_dict.items():
        time.sleep(random.randrange(1, 3))
        req = fetch(f"https://leroymerlin.kz/api/internal/vue/catalogue_section_listing/{key}", {
            "headers": {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en;q=0.9",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Brave\";v=\"108\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "sec-gpc": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "x-language-id": "ru",
                "x-requested-with": "XMLHttpRequest",
                "cookie": "route=b8d38fc23291992830561e0ced87da01; PHPSESSID=3149a9f2f1e3145e123ca0f2b7b8774e; BITRIX_SM_SALE_UID=61766871; geoCommonDisabled=true; catalogSavedSettings={%22displayMode%22:3%2C%22perPage%22:%2210000%22}",
                "Referer": f"{value}",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            },
            "body": "csrf_token=d77d90faaa7ec10b2cc79b3d8181db29&currentPage=1&perPage=10000&collection=&sortField=POPULARITY&sortDirection=desc",
            "method": "POST"
        })

        print(str(count) + ": " + str(req.status_code))
        count += 1
        req_to_json = req.json()
        with open('get_all_urls/extra_json/all_urls_from_lv3.json', 'w', encoding='utf-8') as file:
            json.dump(req_to_json, file, indent=4, ensure_ascii=False)

        with open('get_all_urls/extra_json/all_urls_from_lv3.json', encoding='utf-8') as file:
            one_lv3 = json.load(file)

        products_in_1_lv3 = one_lv3['products']
        for pr in products_in_1_lv3:
            all_urls.append("https://leroymerlin.kz" + pr['URL'])

    print(all_urls)
    print(len(all_urls))


def get_all_product_urls():
    lv1_lv2_get_categories('https://leroymerlin.kz/catalogue/')
    # Откоментировать 2 нижние строчки для проверки собранных категорий 3-го уровня
    # for lv1 in lv1list:
    #     lv3_get_categories(lv1)

    get_urls('https://leroymerlin.kz/catalogue/')


def write_product_urls_to_txt():
    with open('one_product_data/all_products.txt', 'w', encoding='utf-8') as file:
        for line in all_urls:
            file.write(line + '\n')


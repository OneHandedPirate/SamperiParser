from bs4 import BeautifulSoup
import requests
import csv, os
from time import sleep
from random import randint
from datetime import date


try:
    os.mkdir(f'data/categories/{date.today()}')
except:
    pass

def retry(url):
    try:
        retr = requests.get(url, headers=headers).text
        return retr
    except:
        sleep(10)
        retry(url)


URL = 'https://shop.samberi.com/'

headers = {
    'Accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}

def parse():
    try:
        all_products = []
        req = retry(URL)
        bs = BeautifulSoup(req, 'lxml')
        categories = bs.find('ul', id='vertical-multilevel-menu').find_all('a', class_='parent')
        for num, cat in enumerate(categories, start=1):
            cat_list = []
            page_count = 0
            cat_url = 'https://shop.samberi.com' + cat.get('href')
            print(f'\nПарсим категорию {cat.text}...\n')
            req_pages = retry(cat_url)
            ps = BeautifulSoup(req_pages, 'lxml')
            try:
                last_page = ps.find('div', class_='bx-pagination-container row').find_all('li', class_='mit-page-link')[-1].text
            except:
                last_page = 1
            for i in range(1, int(last_page)+1):
                req_page = retry(cat_url + f'?PAGEN_1={i}')
                pagebs = BeautifulSoup(req_page, 'lxml')
                products_on_page = pagebs.find_all('div', class_='product-item')
                for product in products_on_page:
                    name = product.find('div', class_='product-item-title').text.strip()
                    price = product.find('span', class_='product-item-price-current').text.strip().strip('₽').strip()
                    all_products.append([name, price])
                    cat_list.append([name, price])
                page_count += 1
                print(f'Страниц в категории {cat.text} спаршено: {page_count}')
                sleep(randint(1, 3))
            sleep(randint(3, 5))
            # with open(f'data/categories/{date.today()}/{num} {cat.text.replace("/", " ")}.csv', 'w', encoding='utf-8-sig', newline='') as csvt:
            #     writer_cat = csv.writer(csvt, delimiter=',')
            #     for i in cat_list:
            #         writer_cat.writerow([i[0], i[1]])
            print(f'\nСпаршено категорий товаров: {num}')

        with open(f'data/{date.today()}.csv', 'w', encoding='utf-8-sig', newline='') as csvtab:
            writer = csv.writer(csvtab, delimiter=',')
            for product in all_products:
                writer.writerow([product[0], product[1]])

        input('Press Enter to quit')
    except:
        sleep(10)
        os.system('cls')
        parse()


parse()





    


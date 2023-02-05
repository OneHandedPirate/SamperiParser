from bs4 import BeautifulSoup
import csv
import asyncio
import aiohttp
from datetime import date


URL = 'https://shop.samberi.com'

HEADERS = {
    'Accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.54 Safari/537.36'
}

all_products = []
n = 0

async def get_products(url):
    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url, headers=HEADERS)
        bs = BeautifulSoup(await res.text(), 'lxml')
        cats = [URL + cat.get('href') + '?SHOWALL_1=1'
                for cat in bs.find('ul', id='vertical-multilevel-menu')
                .find_all('a', class_='parent')]
        tasks = []
        for cat_url in cats:
            task = asyncio.create_task(parse_page(session, cat_url))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def parse_page(session, cat_url):
    async with session.get(url=cat_url, headers=HEADERS) as res:
        res_text = await res.text()
        pagebs = BeautifulSoup(res_text, 'lxml')
        products_on_page = pagebs.find_all('div', class_='product-item')
        for product in products_on_page:
            name = product.find('div', class_='product-item-title').text.strip()
            price = product.find('span', class_='product-item-price-current')\
                .text.strip().strip('₽').strip()
            all_products.append([name, price])
        global n
        n += 1
        print(f'Категорий спаршено: {n}')

def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_products(URL))

    with open(f'data/{date.today().strftime("%d-%m-%Y")}.csv',
              'w', encoding='utf-8-sig', newline='') as csvtab:
        writer = csv.writer(csvtab, delimiter=',')
        for product in all_products:
            writer.writerow([product[0], product[1]])
    print(f'\n\nРабота завершена.\nВсего товаров: {len(all_products)}', end='')
    input('\n\nНажмите любую клавишу чтобы выйти')


if __name__ == '__main__':
    main()
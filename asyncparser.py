import csv
import asyncio
from datetime import date
from time import time
import aiohttp
from bs4 import BeautifulSoup


URL = 'https://shop.samberi.com'

HEADERS = {
    'Accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.54 Safari/537.36'
}

all_products = []
start_time = time()
n = 0

def progress(step, max_s, elems=30):
    percent = round(step * 100 / max_s)
    graph = f"{'⬜' * round(elems*step/max_s) if step != 0 else ''}"
    print(f'\r[{percent}%] {graph}', end='')


async def get_products(url):

    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url, headers=HEADERS)
        bs = BeautifulSoup(await res.text(), 'lxml')
        cats = [URL + cat.get('href') + '?SHOWALL_1=1'
                for cat in bs.find('ul', id='vertical-multilevel-menu')
                .find_all('a', class_='parent')] + [
            #Костыль, не могу получить эти ссылки автоматически(
            'https://shop.samberi.com/catalog/aziya/?SHOWALL_1=1',
            'https://shop.samberi.com/catalog/sportivnye_tovary/?SHOWALL_1=1',
            'https://shop.samberi.com/catalog/upakovka/?SHOWALL_1=1'
        ]
        max_s = len(cats)
        #tasks = [asyncio.create_task(parse_page(session, url, max_s)) for url in cats]
        tasks = [asyncio.shield(parse_page(session, url, max_s)) for url in cats]

        await asyncio.gather(*tasks)

async def parse_page(session, cat_url, max_s):
    #await asyncio.sleep(abs(r()-0.5))
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
    progress(n, max_s)

def main():
    progress(0, 1)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_products(URL))

    with open(f'data/{date.today().strftime("%d-%m-%Y")}.csv',
              'w', encoding='utf-8-sig', newline='') as csvtab:
        writer = csv.writer(csvtab, delimiter=',')
        for product in all_products:
            writer.writerow([product[0], product[1]])
    print(f'\n\nРабота завершена.\nВсего товаров: {len(all_products)}',
          f'Время выполнения: {round(time() - start_time, 2)} сек.', sep='\n')

    input('\n\nНажмите любую клавишу чтобы выйти')


if __name__ == '__main__':
    main()
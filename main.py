from bs4 import BeautifulSoup

import json
import requests


def run():
    base_url = 'http://books.toscrape.com'
    response = requests.get(base_url)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        all_product_li = soup.find_all('li', attrs={'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

        products = []

        for product_li in all_product_li:
            article = product_li.find('article')

            link = '{}/{}'.format(base_url, article.h3.a.get('href'))

            link_response = requests.get(link)
            link_response.encoding = 'utf-8'

            if link_response.status_code == 200:
                link_soup = BeautifulSoup(link_response.text, 'html.parser')

                product_page = link_soup.find('div', id='content_inner').article

                products.append({
                    'title': article.h3
                        .a
                        .get('title'),

                    'image': '{}/{}'.format(base_url, article.find('div', class_='image_container')
                        .a
                        .img
                        .get('src')),

                    'price': article.find('div', class_='product_price')
                        .find('p', class_='price_color')
                        .text,

                    'status': article.find('div', class_='product_price')
                        .find('p', class_='instock availability')
                        .text
                        .replace('\n', '')
                        .strip(),

                    'link': link,

                    'description': product_page.find_all('p')[3].text
                })

        with open('./books.json', 'w', encoding='utf-8') as books:
            # Persistindo os dados obtidos da página em um arquivo JSON no disco.
            json.dump(products, books, indent=2, ensure_ascii=False)
    else:
        print('Page cannot be loaded.')


if __name__ == '__main__':
    run()

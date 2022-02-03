# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import lxml
import json
import time
from random import randrange

FILE = 'ParseResults.csv'
HOST = 'https://www.citilink.ru/catalog/smartfony/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image'
              '/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_article_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('span', class_='navigations').find_all('a')[-1].text)

    articles_urls_list = []
    for page in range(1, pagination_count + 1):
        response = s.get(url=f'https://hi-tech.news/page/{page}/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        articles_urls = soup.find_all('a', 'post-title-a')
        for au in articles_urls:
            art_url = au.get('href')
            articles_urls_list.append(art_url)
        time.sleep(randrange(2, 5))
        print(f'Обработал {page} страницу из {pagination_count} ')
    with open('articles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'{url}\n')
    return 'Работа по сбору ссылок завершена'


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]
        urls_count = len(urls_list)

        s = requests.Session()
        result_data = []

        for url in enumerate(urls_list):
            response = s.get(url=url[1], headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            article_title = soup.find('div', class_='post-content').find('h1', class_='title').text.strip()
            article_data = soup.find('div', class_='post').find('div', class_='tile-views').text.strip()
            article_img = f"https://hi-tech.news{soup.find('div', class_='post-media-full').find('img').get('src')}"
            article_text = soup.find('div', class_='the-excerpt').text.strip().replace('\n', '')

            result_data.append({
                'Original_url': url[1],
                'Title': article_title,
                'Data': article_data,
                'Img': article_img,
                'Article_Text': article_text,
            })
            # print(f'{article_title}\n{article_data}\n{article_img}\n')
            time.sleep(randrange(1, 2))
            print(f'Обработано {url[0]+1}/{urls_count}')
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    # print(get_article_urls(url='https://hi-tech.news'))
    get_data('articles_urls.txt')


if __name__ == '__main__':
    main()


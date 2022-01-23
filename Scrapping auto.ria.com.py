
import requests
from bs4 import BeautifulSoup
import lxml
import csv
import os

FILE = 'cars.csv'
HOST = 'https://auto.ria.com'
URL = 'https://auto.ria.com/newauto/marka-mg/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50',
    'accept': '*/*'
}

def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    print(req)
    return req

def get_pages_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='na-gallery-view').find_all('section', class_='proposition')
    cars = []
    for item in items:
        uah_price = item.find('span', class_='size16')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Цену уточнайте'
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'link': HOST + item.find('a', class_='proposition_link').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
            'uah_price': uah_price,
            'city': item.find('span', class_='region').get_text(strip=True)
        })
    return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в грн', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])
def parse():
    URL = input('Введите URL: ')
    URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Scrapping page {page} of  {pages_count}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Get {len(cars)} cars')
    else:
        print('Error')
    os.startfile(FILE)
parse()
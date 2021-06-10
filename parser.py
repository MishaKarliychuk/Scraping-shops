import requests
from bs4 import BeautifulSoup
import time
import io
import json

# коментарии
def open_out():
    with open('output.csv', 'r') as f:              # открываем файл output.csv
        sites = ['link', 'rosetka', '1baby', 'ladyshki', 'pampik', 'pipi', 'kotugoroshko','auchan','apteka', 'lindo','agusik','yourhappy']       # нужные сайты
        links = {}
        for i in sites:             # считываем и добавляем все ссылки с файла output.csv в словарь links
            links[i] = f.readline()
        return links
urll = 'https://auchan.ua/graphql/?query=query%20CatalogProducts(%24filter%3A%20ProductFilterInput!%2C%20%24sort%3A%20ProductSortInput%2C%20%24pageSize%3A%20Int!%2C%20%24currentPage%3A%20Int!%2C%20%24priceSet%3A%20Boolean!%2C%20%24filterSet%3A%20Boolean!%2C%20%24sortSet%3A%20Boolean!)%20%7B%0A%20%20products(pageSize%3A%20%24pageSize%2C%20currentPage%3A%20%24currentPage%2C%20filter%3A%20%24filter%2C%20sort%3A%20%24sort)%20%7B%0A%20%20%20%20min_price%20%40include(if%3A%20%24priceSet)%0A%20%20%20%20max_price%20%40include(if%3A%20%24priceSet)%0A%20%20%20%20filters%20%40include(if%3A%20%24filterSet)%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20request_var%0A%20%20%20%20%20%20filter_items_count%0A%20%20%20%20%20%20filter_items%20%7B%0A%20%20%20%20%20%20%20%20label%0A%20%20%20%20%20%20%20%20value_string%0A%20%20%20%20%20%20%20%20items_count%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20sort_fields%20%40include(if%3A%20%24sortSet)%20%7B%0A%20%20%20%20%20%20options%20%7B%0A%20%20%20%20%20%20%20%20label%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20page_info%20%7B%0A%20%20%20%20%20%20total_pages%0A%20%20%20%20%20%20current_page%0A%20%20%20%20%20%20page_size%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20total_count%0A%20%20%20%20items%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20sku%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20brand%0A%20%20%20%20%20%20url_key%0A%20%20%20%20%20%20stock_status%0A%20%20%20%20%20%20type_id%0A%20%20%20%20%20%20thumbnail%20%7B%0A%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%20%20label%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20special_price%0A%20%20%20%20%20%20price%20%7B%0A%20%20%20%20%20%20%20%20regularPrice%20%7B%0A%20%20%20%20%20%20%20%20%20%20amount%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20categories%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20breadcrumbs%20%7B%0A%20%20%20%20%20%20%20%20%20%20id%3A%20category_id%0A%20%20%20%20%20%20%20%20%20%20category_id%0A%20%20%20%20%20%20%20%20%20%20category_name%0A%20%20%20%20%20%20%20%20%20%20category_level%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20offers%20%7B%0A%20%20%20%20%20%20%20%20from_date%0A%20%20%20%20%20%20%20%20to_date%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20product_labels%20%7B%0A%20%20%20%20%20%20%20%20alt%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20image%0A%20%20%20%20%20%20%20%20visible%20%7B%0A%20%20%20%20%20%20%20%20%20%20category%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20position%0A%20%20%20%20%20%20%20%20%20%20%20%20display%0A%20%20%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20...%20on%20ConfigurableProduct%20%7B%0A%20%20%20%20%20%20%20%20configurable_options%20%7B%0A%20%20%20%20%20%20%20%20%20%20attribute_code%0A%20%20%20%20%20%20%20%20%20%20label%0A%20%20%20%20%20%20%20%20%20%20values%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20default_label%0A%20%20%20%20%20%20%20%20%20%20%20%20label%0A%20%20%20%20%20%20%20%20%20%20%20%20store_label%0A%20%20%20%20%20%20%20%20%20%20%20%20use_default_value%0A%20%20%20%20%20%20%20%20%20%20%20%20value_index%0A%20%20%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20product_id%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20variants%20%7B%0A%20%20%20%20%20%20%20%20%20%20product%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20%20%20%20%20price%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20regularPrice%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20amount%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20special_price%0A%20%20%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D%0A&operationName=CatalogProducts&variables=%7B%22sort%22%3A%7B%22special_price%22%3A%22DESC%22%2C%22url_key%22%3A%22ASC%22%7D%2C%22filter%22%3A%7B%22category_id%22%3A%7B%22eq%22%3A2779%7D%7D%2C%22category%22%3A2779%2C%22filterSet%22%3Atrue%2C%22priceSet%22%3Atrue%2C%22sortSet%22%3Atrue%2C%22currentPage%22%3AW%2C%22pageSize%22%3A24%7D'
def write():
    global da, res,links,real
    with io.open('input.csv', 'a') as f:
        for da in res:
            link = u'{l1};'.format(l1=da['link'])
            title = u'{t};'.format(t=str(da['title']))
            f.write(link)
            f.write(title)
            try:
                prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                f.write(prices)
            except:
                prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                f.write(prices)
            f.write('\n')

# коментарии
def import_needed_links(site, tag, count):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    funct = open_out()
    real = funct[site]              # получаем ссылку
    response = requests.get(real, headers=HEADERS)          # делаем запрос по ссылке url
    soup = BeautifulSoup(response.content, 'html.parser')               # получаем html код
    items = soup.findAll(tag)                                       # ищем нужные данные по тэгу
    allLinks = []
    neededLink = []
    for item in items:
        try:
           allLinks.append(item.find('a').get('href'))              # добавляем данные в список  allLinks
        except:
            continue
    for i in range(count):              # это уже индивидуально для каждого сайта
        if i % 2 != 0:
            continue
        else:
            neededLink.append(allLinks[i])
    return neededLink               # возвращаем список со ссылками

# коментарии
def general(times):
    global res, real,links,real
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    # цикл проходит по страницам
    for i in range(1,35):
        ur = 'https://xl-catalog-api.rozetka.com.ua/v3/goods/get?front-type=xl&category_id=2586292&page=W&sort=rank&lang=ua'
        url = ur.replace('W', str(i))
        response = requests.get(url, headers=HEADERS)           # делаем запрос
        soup = BeautifulSoup(response.content, 'html.parser').get_text(strip=True)
        js = json.loads(soup)
        time.sleep(1)
        s = str(js['data']['ids'])
        real = s.replace(' ','')
        real = real[1:-1:]
        url = 'https://xl-catalog-api.rozetka.com.ua/v3/goods/getDetails?front-type=xl&with_groups=1&with_docket=1&goods_group_href=1&product_ids='+ str(real)+ '&lang=ua'
        response = requests.get(url, headers=HEADERS)           # делаем запрос
        soup = BeautifulSoup(response.content, 'html.parser').get_text(strip=True)       # считываем html код с страницы
        js = json.loads(soup)
        res = []
        for q in range(len(js['data'])):
            if str(js['data'][q]['sell_status']) == 'unavailable':
                res.append({                # добавляем нужные данные в список res
                    'link': js['data'][q]['href'],
                    'title' : js['data'][q]['title'],
                    'price': '0',
                    'old_price': '0'
                })
                continue
            if str(js['data'][q]['old_price']):
                res.append({                # добавляем нужные данные в список res
                    'link': js['data'][q]['href'],
                    'title' : js['data'][q]['title'],
                    'price': js['data'][q]['price'],
                    'old_price': js['data'][q]['old_price']
                })
                continue
            else:
                res.append({                # добавляем нужные данные в список res
                    'link': js['data'][q]['href'],
                    'title' : js['data'][q]['title'],
                    'price': js['data'][q]['price'],
                    'old_price': '0'
                })
                continue
        with io.open('input.csv', 'a') as f:
            for da in res:
                link = u'{l1};'.format(l1=da['link'])
                title = u'{t};'.format(t=str(da['title']))
                try:
                    f.write(link)
                    f.write(title)
                except:
                    continue
                try:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                    f.write(prices)
                except:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                    f.write(prices)
                f.write('\n')

def rosetka():
    general(35)
    print('Сайт rosetka спарсен')


def baby1():
    global res
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    for i in range(1, 6):
        time.sleep(1)
        links = open_out()
        real = ''.join(links['1baby'])
        real = real.split(';')
        url = f'{real[0]}{i}'
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll('div', class_='caption')
        res = []
        for item in items:
            res.append({
                'link': item.find('a').get('href'),
                'title': item.find('h4').get_text(strip=True),
                'price': item.find('span', class_='price-new'),
                'old_price': item.find('span', class_='price-old')
            })
        for rem in res:
            if str(rem['price']) == 'None' or str(rem['old_price']) == 'None':
                rem['price'] = 0
                rem['old_price'] =0
            else:
                rem['price'] = str(rem['price'])[24:33:]
                rem['old_price'] =str(rem['old_price'])[24:33:]
        with io.open('input.csv', 'a') as f:
            for da in res:
                link = u'{l1};'.format(l1=da['link'])
                title = u'{t};'.format(t=str(da['title']))
                f.write(link)
                f.write(title)
                try:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                    f.write(prices)
                except:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                    f.write(prices)
                f.write('\n')
    print('Сайт baby1 спарсен')

def ladyshki():
    global res
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    for i in range(1, 32):
        time.sleep(1)
        links = open_out()
        real = links['ladyshki']
        url = str(real).replace('Q', str(i))
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll('div', class_='cs-product-gallery__info-panel')
        res = []
        for item in items:
            if 'Нет в наличии' in str(item.find('span', class_='cs-goods-data__state cs-goods-data__state_val_clarify')) or 'Нет в наличии' in str(item.find('span', class_='cs-goods-price__value cs-goods-price__value_type_old')) or 'None' in str(item.find('span', class_='cs-goods-price__value cs-goods-price__value_type_old')):
                res.append({
                    'link': item.find('a', class_='cs-goods-title').get('href'),
                    'title': item.find('a', class_='cs-goods-title').get_text(strip=True),
                    'price': item.find('span', class_='cs-goods-price__value cs-goods-price__value_type_current').get_text(strip=True),
                    'old_price': '0'
                })
            else:
                res.append({
                'link': item.find('a', class_='cs-goods-title').get('href'),
                'title': item.find('a', class_='cs-goods-title').get_text(strip=True),
                'price': item.find('span', class_='cs-goods-price__value cs-goods-price__value_type_current').get_text(strip=True),
                'old_price': item.find('span', class_='cs-goods-price__value cs-goods-price__value_type_old').get_text(strip=True)
            })
        with io.open('input.csv', 'a') as f:
            for da in res:
                link = u'{l1};'.format(l1=da['link'])
                title = u'{t};'.format(t=str(da['title']))
                f.write(link)
                f.write(title)
                try:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                    f.write(prices)
                except:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                    f.write(prices)
                f.write('\n')
    print('Сайт ladyshki спарсен')

def yourhappy():
    global res
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    for i in range(1):
        time.sleep(1)
        url = import_needed_links('yourhappy','td',28)
        urls = [url[0],str(url[0])+'?ps=200']
        for k in range(2):
            url = urls[k]
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.findAll('div', class_= 'item-container')
            res = []
            for item in items:
                if 'None' in str(item.find('div', class_= 'price through')):
                    res.append({
                    'link': 'https://yourhappy.com.ua/'+item.find('a').get('href'),
                    'title' : item.find('div', class_= 'item-name').get_text(strip=True),
                    'price': item.find('div', class_= 'price t-red strong star').get_text(strip=True),
                    'old_price': '0'
                })
                    continue
                else:
                    res.append({
                    'link': 'https://yourhappy.com.ua/'+item.find('a').get('href'),
                    'title' : item.find('div', class_= 'item-name').get_text(strip=True),
                    'price': item.find('div', class_= 'price t-red strong star').get_text(strip=True),
                    'old_price': item.find('div', class_= 'price through').get_text(strip=True)
                })
                    continue
            with io.open('input.csv', 'a') as f:
                for da in res:
                    link = u'{l1};'.format(l1=da['link'])
                    title = u'{t};'.format(t=str(da['title']))
                    f.write(link)
                    f.write(title)
                    try:
                        prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                        f.write(prices)
                    except:
                        prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                        f.write(prices)
                    f.write('\n')
    for i in range(1,13):
        time.sleep(1)
        url = import_needed_links('yourhappy','td',28)
        url = url[i]
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll('div', class_= 'item-container')
        res = []
        for item in items:
            if 'None' in str(item.find('div', class_= 'price through')):
                res.append({
                'link': 'https://yourhappy.com.ua/'+item.find('a').get('href'),
                'title' : item.find('div', class_= 'item-name').get_text(strip=True),
                'price': item.find('div', class_= 'price t-red strong star').get_text(strip=True),
                'old_price': '0'
            })
                continue
            else:
                res.append({
                'link': 'https://yourhappy.com.ua/'+item.find('a').get('href'),
                'title' : item.find('div', class_= 'item-name').get_text(strip=True),
                'price': item.find('div', class_= 'price t-red strong star').get_text(strip=True),
                'old_price': item.find('div', class_= 'price through').get_text(strip=True)
            })
                continue
        with io.open('input.csv', 'a') as f:
            for da in res:
                link = u'{l1};'.format(l1=da['link'])
                title = u'{t};'.format(t=str(da['title']))
                f.write(link)
                f.write(title)
                try:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                    f.write(prices)
                except:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                    f.write(prices)
                f.write('\n')
    print('Сайт yourhappy спарсен')

def pipi():
    global res
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    for i in range(1):
        time.sleep(1)
        res = []
        k = 0
        links = open_out()
        url = ''.join(links['pipi'])
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll('div', class_='name')
        price = soup.findAll('div', class_='price')
        for item in items[22::]:
            pr = price[k]
            if 'None' in str(pr.find('span', class_= 'price-old')):
                res.append({
                    'link': item.find('a').get('href'),
                    'title' : item.find('a').get_text(strip=True),
                    'price': pr.get_text(strip=True),
                    'old_price': '0'
                })
            else:
                res.append({
                    'link': item.find('a').get('href'),
                    'title' : item.find('a').get_text(strip=True),
                    'price': pr.find('span', class_='price-new').get_text(strip=True),
                    'old_price': pr.find('span', class_='price-old').get_text(strip=True)
                })
            k += 1
        with io.open('input.csv', 'a') as f:
            for da in res:
                link = u'{l1};'.format(l1=da['link'])
                title = u'{t};'.format(t=str(da['title']))
                f.write(link)
                f.write(title)
                try:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                    f.write(prices)
                except:
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                    f.write(prices)
                f.write('\n')
    print('Сайт pipi спарсен')

def kotugoroshko():
    global res
    def import_needed_links2(site, tag):
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        funct = open_out()
        real = funct[site]
        response = requests.get(real, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll(tag)
        allLinks = []
        for item in items:
            try:
                allLinks.append('https://kotugoroshko.kiev.ua/' + item.find('a', class_='cs-product-groups-gallery__image-link').get('href') + '/page_W#catalog_controls_block')
            except:
                continue
        return allLinks
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    urls = import_needed_links2('kotugoroshko','li')
    for k in range(9):
        try:
            url_for_count = urls[k].replace('W','1')
            response = requests.get(url_for_count, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            count_div = soup.findAll('a', class_= 'b-pager__link')
            count_div = count_div[:-1:]
            count = count_div[-1].get_text(strip=True)
        except:
            count = 1
        for q in range(1, int(count)+1):
            time.sleep(1)
            url = urls[k].replace('W', str(q))
            response2 = requests.get(url, headers=HEADERS)
            soup2 = BeautifulSoup(response2.content, 'html.parser')
            items = soup2.findAll('div', class_= 'cs-product-gallery__item-inner')
            res =[]
            for item in items:
                if 'Нет в наличии' in str(item.find('span', class_= 'cs-goods-data__state cs-goods-data__state_val_clarify')):
                    res.append({
                    'link': item.find('a', class_='cs-goods-title').get('href'),
                    'title' : item.find('a', class_= 'cs-goods-title').get_text(strip=True),
                    'price': '0',
                    'old_price': '0'
                })
                elif 'cs-goods-price__value cs-goods-price__value_type_old cs-goods-price__value_type_product-list' in item:
                    res.append({
                    'link': item.find('a', class_='cs-goods-title').get('href'),
                    'title' : item.find('a', class_= 'cs-goods-title').get_text(strip=True),
                    'price': '0',
                    'old_price': item.find('span', class_= 'cs-goods-price__value cs-goods-price__value_type_old cs-goods-price__value_type_product-list').get_text(strip=True)
                })
                else:
                    res.append({
                    'link': item.find('a', class_='cs-goods-title').get('href'),
                    'title' : item.find('a', class_= 'cs-goods-title').get_text(strip=True),
                    'price': item.find('span', class_= 'cs-goods-price__value cs-goods-price__value_type_current cs-goods-price__value_type_product-list').get_text(strip=True),
                    'old_price': '0'
                })
            with io.open('input.csv', 'a') as f:
                for da in res:
                    link = u'{l1};'.format(l1=da['link'])
                    title = u'{t};'.format(t=str(da['title']))
                    f.write(link)
                    f.write(title)
                    try:
                        prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                        f.write(prices)
                    except:
                        prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                        f.write(prices)
                    f.write('\n')
    print('Сайт kotugoroshko спарсен')

# коментарии
def auchan():
    global res, urll
    for k in range(1,27):
        # другая схема, считываем json  и выводим данные
        time.sleep(1)
        links = open_out()
        real = urll
        res = []
        url = real.replace('W', str(k))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser').get_text(strip=True)
        js = json.loads(soup)
        try:
            for i in range(len(js['data']['products']['items'])):
                id = js['data']['products']['items'][i]['id']
                if js['data']['products']['items'][i]['stock_status'] == 'OUT_OF_STOCK':            # если товара нету в наличии
                    res.append({
                            'link': 'https://auchan.ua/ua/'+js['data']['products']['items'][i]['url_key']+'-'+str(id),
                            'title' : js['data']['products']['items'][i]['name'],
                            'price': '0',
                            'old_price': '0'
                        })
                    continue
                elif 'None' in str(js['data']['products']['items'][i]['special_price']):            # если старой цены нету
                    res.append({
                            'link': 'https://auchan.ua/ua/'+js['data']['products']['items'][i]['url_key']+'-'+str(id),
                            'title' : js['data']['products']['items'][i]['name'],
                            'price': js['data']['products']['items'][i]['price']['regularPrice']['amount']['value'],
                            'old_price': '0',
                        })
                    continue
                else:                   # если все ок (старая цена есть, товар в наличии)
                    res.append({
                            'link': 'https://auchan.ua/ua/'+js['data']['products']['items'][i]['url_key']+'-'+str(id),
                            'title' : js['data']['products']['items'][i]['name'],
                            'price': js['data']['products']['items'][i]['special_price'],
                            'old_price': js['data']['products']['items'][i]['price']['regularPrice']['amount']['value'],
                        })
                    continue
            with io.open('input.csv', 'a') as f:
                for da in res:
                    link = u'{l1};'.format(l1=da['link'])
                    title = u'{t};'.format(t=str(da['title']))
                    f.write(link)
                    f.write(title)
                    try:
                        prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                        f.write(prices)
                    except:
                        prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'][:-1:])
                        f.write(prices)
                    f.write('\n')
        except:
            continue
    print('Сайт auchan спарсен')

def apteka():
    global res
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    def import_needed_links3(site, tag):
        links = open_out()
        real = ''.join(links[site])
        real = real[:-1:]
        response = requests.get(real, headers=headers, allow_redirects=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        it = soup.findAll(tag, class_='block-groups-list g-overflow')
        try:
            items = it[0].findAll('li')
        except:
            return ['aaa',',,,','ssss']
        allLinks = []
        for item in items:
            try:
                allLinks.append(item.find('a').get('href'))
            except:
                continue
        return list(allLinks[:1:]+allLinks[6:7:]+allLinks[14:15:]+allLinks[20:21:]+allLinks[27:28:]+allLinks[34:35:]+allLinks[39:40:])
    urls = import_needed_links3('apteka','div')
    for k in range(7):
        try:
            url_for_count = urls[k]
            response = requests.get(url_for_count)
            soup = BeautifulSoup(response.content, 'html.parser')
            count_div = soup.findAll('div', class_= 'mb30')
            counts = count_div[-1].find('ul', class_='pagination').get_text(strip=True)
            count = counts[-1]
        except:
            count=1
        for q in range(1, int(count)+1):
            time.sleep(1)
            url = urls[k]+'/page=W'.replace('W', str(q))
            try:
                response2 = requests.get(url, headers=headers)
            except:
                break
            soup2 = BeautifulSoup(response2.content, 'html.parser')
            items = soup2.findAll('div', class_= 'b-prod__bottom')
            res =[]
            for item in items:
                l = item.find('p', class_='prod__header')
                if 'Нет в наличии' in str(item.find('div', class_= 'b-prod__notavail')):
                    res.append({
                    'link': l.find('a').get('href'),
                    'title' : item.find('p', class_= 'prod__header').get_text(strip=True),
                    'price': '0',
                    'old_price': '0'
                })
                    continue
                elif 'price-old' in str(item.find('div', class_= 'b-prod__price')):
                    res.append({
                    'link': l.find('a').get('href'),
                    'title' : item.find('p', class_= 'prod__header').get_text(strip=True),
                    'price': item.find('div', class_= 'price-new').get_text(strip=True),
                    'old_price': item.find('div', class_= 'price-old').get_text(strip=True)
                })
                    continue
                else:
                    res.append({
                    'link': l.find('a').get('href'),
                    'title' : item.find('p', class_= 'prod__header').get_text(strip=True),
                    'price': item.find('div', class_= 'price-new').get_text(strip=True),
                    'old_price': '0'
                })
                    continue
            write()
    print('Сайт apteka спарсен')

def lindo():
    global res
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    def import_needed_links4(site, tag):
        funct = open_out()
        real = ''.join(funct[site])
        real = real.split('\n')
        response = requests.get(real[0], headers=headers, allow_redirects=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll(tag, class_='product-category')
        allLinks = []
        for item in items:
            allLinks.append(item.find('a').get('href'))
        return allLinks
    urls = import_needed_links4('lindo','li')
    for k in range(len(urls)):
        for q in range(1):
            time.sleep(1)
            url = urls[k]+'?count=36&paged='
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.findAll('div', class_= 'product-inner')
            res =[]
            for item in items:
                if 'Нет в наличии' in str(item.find('div', class_= 'b-prod__notavail')):
                    res.append({
                    'link': item.find('a', class_='product-loop-title').get('href'),
                    'title' : item.find('h3', class_= 'woocommerce-loop-product__title').get_text(strip=True),
                    'price': '0',
                    'old_price': '0'
                })
                    continue
                elif 'price-old' in str(item.find('div', class_= 'b-prod__price')):
                    res.append({
                    'link': item.find('a', class_='product-loop-title').get('href'),
                    'title' : item.find('h3', class_= 'woocommerce-loop-product__title').get_text(strip=True),
                    'price': item.find('span', class_= 'woocommerce-Price-amount amount').get_text(strip=True),
                    'old_price': '0'
                })
                    continue
                else:
                    res.append({
                    'link': item.find('a', class_='product-loop-title').get('href'),
                    'title' : item.find('h3', class_= 'woocommerce-loop-product__title').get_text(strip=True),
                    'price': item.find('span', class_= 'woocommerce-Price-amount amount').get_text(strip=True),
                    'old_price': '0'
                })
                    continue
            write()
    print('Сайт lindo спарсен')

from selenium import webdriver
def agusik():
    funct = open_out()
    real = ''.join(funct['agusik'])
    urls = real.split('\n')
    urls = ''.join(urls)
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options = options)
    for l in range(1,19):
        url = urls.replace('W', str(l))
        driver.get(url)
        time.sleep(4)
        res = []
        link = driver.find_elements_by_class_name('product-name')
        title = driver.find_elements_by_class_name('product-name-container')
        price = driver.find_elements_by_class_name('content_price')
        real_p = 0
        old_price = 0
        for i in range(len(title)):
            if len(list(price[i].text)) > 14:
                temp = list(price[i].text)
                real_p = ''.join(temp[:temp.index('.'):])
                for q in temp:
                    if q == '.':
                        old_price = ''.join(temp[temp.index('.')+2:-1:])
            else:
                real_p = price[i].text
                old_price = 0
            res.append({
                'link': link[i+1].get_attribute("href"),
                'title': title[i].text,
                'price': real_p,
                'old_price': old_price
            })
        with io.open('input.csv', 'a') as f:
            for da in res:
                try:
                    link = u'{l1};'.format(l1=da['link'])
                    title = u'{t};'.format(t=str(da['title']))
                    prices = u'{p1};{p2};'.format(p1=da['price'], p2=da['old_price'])
                    f.write(link)
                    f.write(title)
                    f.write(prices)
                    f.write('\n')
                except:
                    continue
    driver.quit()

agusik()

def start():
    rosetka()
    baby1()
    ladyshki()
    yourhappy()
    pipi()
    kotugoroshko()
    auchan()
    apteka()
    lindo()
    agusik()

# Щоб запустити, то розкоментуйте рядок нижче
#start()

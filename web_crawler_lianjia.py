from bs4 import BeautifulSoup
import requests
import time
import json
import csv


def get_rentdate(url):
    #url = 'https://sh.lianjia.com/zufang/SH0004801043.html'
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')

    '''
    ## Another way to get the info.
    title_list = soup.select('h1.main')
    title = title_list[0].text
    print(title)
    '''
    images = soup.select('#topImg > div.imgContainer > img')
    titles = soup.select('body > div > div.title-wrapper > div > div.title > h1')
    prices = soup.select('body > div > div.overview > div.content.zf-content > div.price > span.total')
    names = soup.select('body > div > div.overview > div.content.zf-content > div.brokerInfo > div > div.brokerName > a.name.LOGCLICK')
    tels = soup.select('body > div > div.overview > div.content.zf-content > div.brokerInfo > div > div.phone')
    for images, titles, prices, names, tels in zip(images, titles, prices, names, tels):
        data = {
            'images': images.get("src"),
            'titles': titles.get_text(),
            'prices': prices.get_text(),
            'names': names.get_text(),
            'tels': tels.get_text(strip=True),
        }
        #print(data)
        # sent to local json file
        #write_to_jsonfile(data)
        write_to_csvfile(data)

def write_to_jsonfile(data):
    file_name = 'E:/python_work/web_crawler/week1/1_3/1_3answer_of_homework/data.json'
    with open(file_name, 'a', newline='', encoding='utf-8-sig') as f:
        data_json = json.dumps(data, skipkeys='str')
        f.write(data_json)

def write_to_csvfile(data):
    file_name = 'E:/python_work/web_crawler/week1/1_3/1_3answer_of_homework/data.csv'
    with open(file_name, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        for key, value in data.items():
            writer.writerow([key,value])


def get_rentdata_all(url_page):
    web_data = requests.get(url_page)
    soup = BeautifulSoup(web_data.text, 'lxml')
    hrefs_list = soup.select('h2 > a')
    for href in hrefs_list:
        url = href.get('href')
        get_rentdate(url)


##mian function
urls = ['https://sh.lianjia.com/zufang/pg{}/'.format(str(i)) for i in range(1,101,1)]
for url_page in urls:
    get_rentdata_all(url_page)
    time.sleep(2)
import csv
import bs4
import requests
from bs4 import BeautifulSoup
from datetime import date
from dateutil.relativedelta import relativedelta


cookies = {
    'T': 'TI158297589160700261334285753604456059230319069306856372425800020908',
    'AMCV_17EB401053DAF4840A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C18399%7CMCMID%7C44291356426448143490392995888974852499%7CMCAAMLH-1590237680%7C12%7CMCAAMB-1590237680%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589640080s%7CNONE%7CMCAID%7CNONE',
    'qH': '0258c7d48242959a',
    's_cc': 'true',
    's_sq': '%5B%5BB%5D%5D',
    'S': 'd1t11Pz9BJD8/Pz87PxE/aj91H/cIc/ME5qRocQit/GoyOxLedavOQTkRi2nwi6GN6LEWr1eq/mFqDbiEFT8vM4fQiw==',
    'SN': 'VIE1EB627AE3B64A65AF877B7F12D030EE.TOK26D39B7737C04C7B849AA58ADD743DC4.1589745458.LO',
    'gpv_pn': 'CLP%3Amobile-phones-store',
    'gpv_pn_t': 'FLIPKART%3ACLP',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.google.com/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

params = (
    ('otracker', 'nmenu_sub_Electronics_0_Mobiles'),
)


csv_file = open("only_one_view_all_category.csv", 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['review date ', 'reviews'])


response = requests.get('https://www.flipkart.com/mobile-phones-store', headers=headers, params=params, cookies=cookies)
soup = BeautifulSoup(response.text, 'html.parser')

list_of_all_links = []
# create all link and append it to list_of_all_links list
for links in soup.find_all('a'):
    link = links.get('href')
    list_of_all_links.append("https://www.flipkart.com" + link)

# remove unuseful links from the top and bottom
usefull_links = []#list_of_all_links[31:39]       # todo [31:39]  Latest Launches

for i in range(43, 51):
    usefull_links.append(list_of_all_links[i])  # todo [43,51] best selling phones

for i in range(55, 63):
    usefull_links.append(list_of_all_links[i])  # todo [55,63] selfie camera phones

for i in range(64, 71):                         # todo [64,72] best battery phone
    usefull_links.append(list_of_all_links[i])

# print(usefull_links)

# del list_of_all_links[0:30]   we can also use this method
# del list_of_all_links[8:]     to extract usefull links but is is slow

def remove_emoji(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def date_cal(date_sample):
    if date_sample[0].isdigit():
        if date_sample[1].isdigit():
            num = int(date_sample[0] + date_sample[1])

            x = calci(date_sample[2], num)

            return x
        else:
            num = int(date_sample[0])

            x = calci(date_sample[1], num)
            return x
    else:

        x = date.today()
        return x

def calci(date_sample, num):
    if date_sample == 'y':
        final_date = date.today() + relativedelta(years=-num)
        return final_date
    elif date_sample == 'm':
        final_date = date.today() + relativedelta(months=-num)
        return final_date
    elif date_sample == 'd':
        final_date = date.today() + relativedelta(days=-num)
        return final_date


def review(review_link):
    a = review_link
    i = 2
    try:
        while True:
            print('top a ', a)
            response_review = requests.get(a)
            soup_review = bs4.BeautifulSoup(response_review.text, "html.parser")
            item = soup_review.findAll('div', class_="col _390CkK _1gY8H-")

            review_date = soup_review.findAll('p', {'class': '_3LYOAd'})
            time_of_review = review_date[-1].getText()
            print(time_of_review)
            date_final_review = date_cal(time_of_review)
            print(date_final_review)


            for r in item:
                review = r.find("div", class_="qwjRop")
                rev = review.div.div.text
                print(rev)
                csv_writer.writerow([date_final_review, rev])

            nextpage = soup_review.find("a", class_='_3fVaIS')['href']


            next_link = "https://www.flipkart.com" + nextpage +"&page="+str(i)
            i=i+1
            print('i',i)
            print("next link", next_link)
            a = next_link
            print('bottom a ', a)
            if not nextpage:
                break
    except:
        pass


try:
    while len(usefull_links) > 0:  # while we have urls to crawl
        url = usefull_links.pop(0)  # removes the first element from the list of urls
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        name = soup.find('span', {'class': '_35KyD6'}).getText()
        price = soup.find('div', {'class': '_1vC4OE _3qQ9m1'}).getText()
        warranty = soup.find('div', {'class': '_3h7IGd'}).getText()
        ratting = soup.find('div', {'class': '_1i0wk8'}).getText()
        print(name)
        print(price)
        print(warranty)
        print(ratting)
        review_div = soup.findAll('div', {'class': 'col _39LH-M'})                 #take all the lin k in the div
        for link in review_div:
            l = link.findAll('a')
            for a in l[-1:]:
                review_link = "https://www.flipkart.com"+a['href']

        print(review_link)
        review(review_link)
        print("---------------------------------------------farman------------------------------------------")
except:
    pass

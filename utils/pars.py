import requests
from bs4 import BeautifulSoup


def get_html(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    return response.text


def proccessing(html):
    soup = BeautifulSoup(html, 'lxml').find(
        'div', {'class': 'blockquote-classic'}).text

    data = []

    for item in soup.split('\n'):
        if item == '':
            continue
        else:
            data.append(item.strip().replace('\xa0', ' '))

    return " ".join(data)


def main_pars(target_currency, rate):
    url = f"https://kursolog.com/kzt/{target_currency}/{rate}"
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0"
    }

    html = get_html(url, headers)

    if html is None:
        return

    soup = proccessing(html)

    return soup

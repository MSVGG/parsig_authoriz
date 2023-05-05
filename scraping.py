from requests import Session
from bs4 import BeautifulSoup
from time import sleep


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
           'Referer': 'localhost', 'Connection': 'close', 'Accept-Language': 'ru', 'Accept-Encoding': 'gzip'}
root_url = "https://quotes.toscrape.com/"
login = "https://quotes.toscrape.com/login"


work = Session()
DELAY_S = 0.1


def post(t):
    # словарь с данный для POST запроса
    data = {'csrf_token': t, 'username': '123', 'password': '124', }
    return data


# имитация входа на сайт
work.get(root_url, headers=headers)
sleep(DELAY_S)

# имитация авторизации (на странице авторизации)
# парсим страницу и достаем из нее токен
responce = work.get(login, headers=headers)
soup = BeautifulSoup(responce.text, 'lxml')
token = soup.find("form").find('input').get('value')

# передаем через POST запрос словарь данных (data)
# и так как POST и GET запросы перенаправление не поддерживают (блокирую поумолчанию)
# разрешаем перенаправление - allow_redirects=True (что бы на перебросило на главную страницу сайта)
result = work.post(login, headers=headers,
                   data=post(token), allow_redirects=True)


def array():
    for number in range(1, 14):
        # нужно написать условие, что бы происходила остановка перебора страниц
        # если контента на странице нет
        # (возможно по кнопке "Next" - если её нет, то на следующую страницу не переходить)
        response = work.get(f"{root_url}page/{number}/", headers=headers)
        sleep(DELAY_S)
        # дописать функцию и убрать туда все однотипные действия
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_="quote")
        for i in data:
            text_card = i.find('span', class_='text').text
            author = i.find('small', class_='author').text
            url_info_author = root_url + i.find('a').get('href')
            # born = pars_info_author(url_info_author)[0]
            # born_location = pars_info_author(url_info_author)[1]
            yield author, text_card, url_info_author, pars_info_author(url_info_author)[0], pars_info_author(url_info_author)[1]


def pars_info_author(url):
    response = work.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('div', class_="author-details")
    born = data.find('p').find('span', class_='author-born-date').text
    born_location = data.find('p').find(
        'span', class_='author-born-location').text
    return born, born_location

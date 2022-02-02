import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    # Передадим в table содержимое таблицы с новостями
    table = parser.find('table', {'class': 'itemlist'})

    # список заголовков
    titles = [i.text for i in table.find_all('a', {'class': 'titlelink'})]
    # списки ссылок
    urls = [i['href'] for i in table.find_all('a', {'class': 'titlelink'})]
    # список авторов
    authors = [i.text for i in table.find_all('a', {'class': 'hnuser'})]
    # список количества лайков
    points = [int(''.join(s for s in i.text if s.isdigit())) for i in table.find_all('span', {'class': 'score'})]
    # список количества комментариев
    comments = []

    for i in table.find_all('td', {'class': 'subtext'}):
        # проверяем, есть ли у новости комментарии
        temp = i.find_all('a')[-1].text
        # если в теге содержится информации о количестве комментариев
        if 'comment' in temp:
            comments.append(int(''.join(s for s in temp if s.isdigit())))
        # если комментариев нет, то пишем, что их 0 :)
        else:
            comments.append(0)

    # список словарей со статьями
    for i in range(len(authors)):
        news_list.append({
            'author': authors[i],
            'comments': comments[i],
            'points': points[i],
            'title': titles[i],
            'url': urls[i]})
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.find('a', {'class': 'morelink'})['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

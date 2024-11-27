from pprint import pprint

import bs4
import requests
import re


def search_data(keys):
    search_url = 'https://habr.com/ru/articles/'
    base_url = 'https://habr.com'
    response = requests.get(search_url)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    articles = soup.select('.tm-articles-list__item')
    parsed_data = []
    pattern = r'|'.join(keys) + r'+'
    for article in articles:
        link = base_url + article.select_one('a.tm-title__link')['href']
        article_response = requests.get(link)
        article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')
        body_soup = article_soup.select_one('div.tm-article-presenter__body')
        article_text = body_soup.select_one('div.article-formatted-body').text
        res = re.search(pattern, article_text, re.IGNORECASE)
        if res:
            header = body_soup.select_one('h1').text
            published_time = body_soup.select_one('time')['title']
            parsed_data.append({
                'title': header,
                'time': published_time,
                'link': link
            })
    return parsed_data


if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'net', 'python', 'кит']
    pprint(search_data(KEYWORDS))




from bs4 import BeautifulSoup
import requests


def team_russia(url_sportbox):
    team_russia_dict = {}
    html_team = requests.get(url_sportbox).text
    sp = BeautifulSoup(html_team, 'lxml')
    all_team = sp.find_all('ul', class_="russia")[0].find_all('li')
    for i in all_team:
        team_russia_dict[i.text.lower()] = i.a.get("href")
    return team_russia_dict


def get_text_article(article_url):
    text_formated = ''
    text_article = requests.get(article_url)
    soup3 = BeautifulSoup(text_article.text, 'lxml')
    text = soup3.find_all('p')
    for i in text:
        if i.a is not None:
            a_tag = i.find_all('a')
            for j in a_tag:
                j.unwrap()
    for i in text:
        text_formated += i.get_text()+'\n'
    return text_formated


def my_text(url, count):
    pages = requests.get(url)
    soup = BeautifulSoup(pages.text, 'lxml')
    dict1 = {}
    if count == 30:
        return "Новостей больше нет"
    articles = soup.find_all('span', class_="text")[count:count+3]
    text = soup.find_all('div', class_="_Sportbox_Spb2015_Components_TeazerBlock_TeazerBlock")[count:count+3]
    for article in range(len(articles)):
        dict1[articles[article].get_text()] = (get_text_article('https://news.sportbox.ru' + text[article].find('a').get("href")),
                                               'https://news.sportbox.ru' + text[article].find('a').get("href"))
    return dict1


team = team_russia('https://news.sportbox.ru/Vidy_sporta/Futbol/Russia')


def pretty_news_message(my_team, count):
    if my_team.lower() in team:
        url = 'https://news.sportbox.ru'+team[my_team.lower()]+"/news"
        team_news = my_text(url, count)
        return team_news
    else:
        return "Введите команду из РПЛ"

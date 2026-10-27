import requests
from bs4 import BeautifulSoup
import time

from logger import logger

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_dir, 'parser.log')

@logger(log_path)
def get_html(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Ошибка при получении страницы: {response.status_code}")
        return None


@logger(log_path)
def parse_articles(html):
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='tm-articles-list__item')
    
    print(f"Найдено статей на странице: {len(articles)}")
    print(f"Ключевые слова для поиска: {KEYWORDS}\n")
    
    matched_articles = []
    
    for i, article in enumerate(articles):
        title_tag = article.find('h2', class_='tm-title')
        title = title_tag.get_text(strip=True) if title_tag else ''
        
        link_tag = title_tag.find('a') if title_tag else None
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else ''
        if link.startswith('/'):
            link = 'https://habr.com' + link
        
        time_tag = article.find('time')
        date = time_tag.get_text(strip=True) if time_tag else ''
        
        full_text = ''
        try:
            time.sleep(1) # пауза без бана
            
            response = requests.get(link, headers=HEADERS)
            if response.status_code == 200:
                article_soup = BeautifulSoup(response.text, 'html.parser')
                full_body = article_soup.find('div', class_='article-formatted-body') or article_soup.find('div', id='post-content-body')
                if full_body:
                    full_text = full_body.get_text(strip=True)
        except Exception as e:
            print(f"Ошибка при загрузке статьи: {e}")
        
        text_to_search = full_text.lower()
        is_match = any(keyword.lower() in text_to_search for keyword in KEYWORDS)
        
        if is_match:
            matched_articles.append({'date': date, 'title': title, 'link': link})
            print(f"НАЙДЕНО: {date} – {title}")
    
    print(f"\nВсего найдено подходящих статей: {len(matched_articles)}")
    return matched_articles

if __name__ == '__main__':
    print("Запуск парсера...")
    html = get_html(URL)
    if html:
        results = parse_articles(html)
        print("Парсинг завершен. Проверь файл parser.log в этой же папке!")
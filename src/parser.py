from requests import get
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import re

def html_scrape(url: str) -> list[str]:
    ua = UserAgent()
    response = get(url, timeout=5, headers={'User-Agent': ua.random})
    response.raise_for_status()

    root = BeautifulSoup(response.text, 'lxml')
    return transform_data(root)


def transform_data(book: BeautifulSoup) -> list[str]:
    book_words = []
    chapters =book.find_all('div', class_ = 'chapter')
    if not chapters:
        raise ValueError('No book chapters were found. The website layout may have changed')
    for chapter in chapters:
        text = chapter.get_text(strip=True).lower()
        chapter_words = re.compile(r"[a-zA-Z]+(?:'[a-zA-Z]+)?").findall(text)
        book_words.extend(chapter_words)
    return book_words

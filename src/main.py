from fetch import html_scrape
from analysis import book_statistics, build_word_counter
from console import play_console, pick_book
from config import urls
import db

if __name__ == '__main__':
    # Подключаемся и инициализируем бд
    conn = db.get_connection()
    db.init_db(conn)
    # Если бд пустая, то заполняем ее книгами из списка
    if db.has_books(conn) is False:
        for book, url in urls.items():
            book_id = db.add_book(conn=conn, title=book, url=url)
            book_list = html_scrape(url=url)
            total_words, reading_time, unique_words = book_statistics(book_list)
            db.add_book_stats(conn=conn, book_id=book_id, total_words=total_words, reading_time=reading_time, unique_words=unique_words)
            word_counts = build_word_counter(book_list)
            db.add_word_stats(conn=conn, book_id=book_id, word_counts=word_counts)

    print('Hello!')
    books_dict = db.get_books(conn=conn)
    while True:
        book_id = pick_book(books_dict)
        if book_id is None:
             exit()
        play_console(conn=conn, book_id=book_id)


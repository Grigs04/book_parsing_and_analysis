import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
from config import DB_PATH

def get_connection() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            url TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_stats (
            book_id INTEGER PRIMARY KEY,
            total_words INTEGER NOT NULL,
            reading_time INTEGER NOT NULL,
            unique_words INTEGER NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS word_stats (
            book_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            count INTEGER NOT NULL,
            PRIMARY KEY (book_id, word),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    conn.commit()



def has_books(conn: sqlite3.Connection) -> bool:
    # Проверяет, есть ли хотя бы одна книга в БД. Используется для первой инициализации.
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM books LIMIT 1")
    return cursor.fetchone() is not None



def add_book(conn: sqlite3.Connection, title: str, url: str) -> int:
    # Добавляет книгу и возвращает её id.
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, url) VALUES (?, ?)",
        (title, url)
    )
    conn.commit()
    return cursor.lastrowid


def add_book_stats(conn: sqlite3.Connection,
                   book_id: int,
                   total_words: int,
                   reading_time: int,
                   unique_words: int) -> None:

    # Сохраняет агрегированную статистику книги.

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO book_stats (book_id, total_words, reading_time, unique_words)
        VALUES (?, ?, ?, ?)
        """,
        (book_id, total_words, reading_time, unique_words)
    )
    conn.commit()


def add_word_stats(conn: sqlite3.Connection,
                   book_id: int,
                   word_counts: Dict[str, int]) -> None:

    # Сохраняет статистику слов одной книги. Использует batch-вставку.
    cursor = conn.cursor()

    rows = [
        (book_id, word, count)
        for word, count in word_counts.items()
    ]

    cursor.executemany(
        """
        INSERT INTO word_stats (book_id, word, count)
        VALUES (?, ?, ?)
        """,
        rows
    )

    conn.commit()



def get_books(conn: sqlite3.Connection) -> Dict[str, str]:

    # Возвращает список доступных книг (id, title).
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM books ORDER BY id")
    result = cursor.fetchall()
    return {str(book_id): book_name for book_id, book_name in result}


def get_book_url(conn: sqlite3.Connection, book_id: int) -> str:

    # Возвращает URL книги по id.
    cursor = conn.cursor()
    cursor.execute(
        "SELECT url FROM books WHERE id = ?",
        (book_id,)
    )
    row = cursor.fetchone()
    return row[0] if row else ""


def get_book_stats(conn: sqlite3.Connection, book_id: int) -> Tuple[int, int, int]:

    # Возвращает (total_words, unique_words).
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT total_words, reading_time, unique_words
        FROM book_stats
        WHERE book_id = ?
        """,
        (book_id,)
    )
    row = cursor.fetchone()
    return row if row else (0, 0, 0)


def get_top_words(conn: sqlite3.Connection,
                  book_id: int) -> List[Tuple[str, int]]:

    # Возвращает список слов книги и их количества.
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT word, count
        FROM word_stats
        WHERE book_id = ? 
        ORDER BY count DESC
        """,
        (book_id,)
    )
    return cursor.fetchall()


def get_word_count(conn: sqlite3.Connection,
                   book_id: int,
                   word: str) -> int | None:

    # Возвращает количество вхождений слова в книге.
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT count
        FROM word_stats
        WHERE book_id = ? AND word = ?
        """,
        (book_id, word)
    )
    row = cursor.fetchone()
    return row[0] if row else None

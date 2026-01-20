from typing import Tuple
import math


def build_word_counter(book_words: list) -> dict[str, int]:
    word_cnt = {}
    for word in book_words:
        word_cnt[word] = word_cnt.get(word, 0) + 1
    return word_cnt

def book_statistics(book: list[str]) -> Tuple[int, int, int]:
    book_length = len(book)
    reading_time = math.ceil(book_length/120)
    cnt_uniq_words = len(set(book))
    return book_length, reading_time, cnt_uniq_words


if __name__ == '__main__':
    print('What? Start on main.py')
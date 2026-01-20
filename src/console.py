import db
import sqlite3
from config import stop_words

def play_console(conn: sqlite3.Connection, book_id: str):

    while True:
        choice = show_menu()
        match choice:
            case '1': print(f'The book is available at the link {db.get_book_url(conn=conn, book_id=int(book_id))}\n')

            case '2':
                word_stats = db.get_book_stats(conn=conn, book_id=int(book_id))
                top_10_words = db.get_top_words(conn=conn, book_id=int(book_id))
                print(f'Length of the book: {word_stats[0]} words',
                      f'Reading time: {word_stats[1]} minutes',
                      f'There are {word_stats[2]} unique words in the book',
                      'Top 10 words in the book:',
                      sep='\n')
                stop_words_set = set(stop_words)
                filtered = ((word, cnt) for word, cnt in top_10_words if word not in stop_words_set)

                for i, (word, cnt) in enumerate(filtered, start=1):
                    if i > 10:
                        break
                    print(f'{i}. {word} — {cnt} times')


            case '3':
                word = input('What word are you interested in?\n').lower()
                word_cnt = db.get_word_count(conn=conn, book_id=int(book_id), word=word)
                if word_cnt is None: print('There is no such word in the book:(')
                else: print(f'The word {word} appears {word_cnt} times in the book.\n')

            case '4': return

            case '5': print('Bye!'), exit()

            case _: print('There is no such function\n')

def pick_book(books: dict) -> str | None:
    exit_option = str(len(books) + 1)

    while True:
        print('Choose book:')
        for num, title in books.items():
            print(f'{num} — {title}')
        print(f'{exit_option} — Exit')

        pick_number = input('Enter option number: ').strip()

        if pick_number == exit_option:
            print('Bye!')
            return None

        if pick_number not in books:
            print('There is no such option. Try again.')
            continue

        return pick_number


def show_menu() -> str:
    print(
          '\nChoose an option',
          '1 — Get book text',
          '2 — Show book statistics',
          '3 — Check word frequency',
          '4 — Choose another book',
          '5 — Exit',
          sep='\n',
          end='\n'
    )
    return input('Enter option number: ').strip()



if __name__ == '__main__':
    print('What? Start on main.py')
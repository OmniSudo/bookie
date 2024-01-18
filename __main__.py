import os
import sys
import database
from tqdm import tqdm
import re  # Added this import for regular expressions


def __main__():
    title = sys.argv[1] if len(sys.argv) > 1 else input("Title: ")
    author = sys.argv[2] if len(sys.argv) > 2 else input("Author: ")
    owner = sys.argv[3] if len(sys.argv) > 3 else input("Owner: ")

    if not os.path.isdir(f"../../{owner}/Books/{title} - {author}"):
        print("Book not found")
        return

    db = database.connect_to_database()

    database.series_table.create(db)
    database.book_table.create(db)
    database.chapter_table.create(db)
    database.word_table.create(db)

    series = database.series_table.insert_series(db, title, author)

    books = database.book_table.get_books_in_filesystem(f"../../{owner}/Books/{title} - {author}")
    for book_data in books:
        book_id = book_data[0]
        book = book_data[1]
        book_path = book_data[2]
        database.book_table.insert_book(db, series, book_id, book)

        print("Processing book ", book_path)

        for file in os.listdir(book_path):
            chapter_words = file.split(' ')
            for i in range(len(chapter_words)):
                if chapter_words[i].isdigit():
                    break
            chapter = ' '.join(chapter_words[i + 1:])
            try:
                i = re.findall(r'\d+', file)
                if i is None or len(i) == 0:
                    print(f"\tSkipping {file} because it does not appear to have a chapter number")
                    continue
                chapter_id = int(i[0])  # Extract the first number in the file path

                if chapter_id == 0:
                    continue

                database.chapter_table.insert_chapter(db, series, book_id, chapter_id, chapter)

                with open(f"{book_path}/{file}", encoding='utf-8') as f:
                    lines = [line.strip('\n') for line in f.readlines()]
                    word_id = 0
                    for line_id in tqdm(range(len(lines)), desc=f"Chapter {chapter_id}"):
                        line = lines[line_id]
                        if line.startswith('##'):
                            continue

                        words = line.split(' ')

                        link = False
                        for word in words:
                            if word.startswith('[[') or link:
                                link = True
                                if word.endswith(']]'):
                                    link = False
                                else:
                                    continue
                            word_id += 1
                            database.word_table.insert_word(db, series, book_id, chapter_id, word_id, word)
            except:
                continue
    db.commit()
    db.close()


if __name__ == "__main__":
    __main__()

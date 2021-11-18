#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2021-11-18
@note    0.0.1 (2021-11-18) : Init file
'''
from __future__ import annotations

from dotenv import load_dotenv

from file.csv_writter import CsvWritter
from scraping.web_scraper import WebScraper

load_dotenv()


class App:
    def __init__(self,) -> None:
        '''Constructor'''

        self.scraper: WebScraper = WebScraper()
        self.csv_writter: CsvWritter = CsvWritter()

    def run(self) -> None:
        '''Main function'''

        categories = self.scraper.get_category_list()
        categories = ['catalogue/category/books/young-adult_21/index.html']
        for category in categories:
            full_books_data = []
            books = self.scraper.get_book_list(category)
            for book in books:
                full_books_data.append(self.scraper.get_book_data(book, category))
            self.csv_writter.write(full_books_data)
            for book_data in full_books_data:
                # self.scraper.download_file(book_data['image_url'])
                ...


def main():
    '''Main function'''
    app: App = App()
    app.run()


if __name__ == '__main__':
    main()

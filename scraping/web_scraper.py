#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2021-11-18
@note    0.0.1 (2021-11-18) : Init file
'''
from __future__ import annotations

import html
import urllib.request
from os import getenv
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self) -> None:
        '''Constructor'''

        self.base_url: str = getenv('URL')
        self.images_directory: Path = Path(__file__).resolve().parent.parent / getenv(
            "IMAGES_DIR"
        )
        self.images_directory.mkdir(parents=False, exist_ok=True)

    def _get_html_page(self, url: str) -> str:
        '''Method Description.
        Description details here (if needed).
        
        Args:
            name (type): Description. Default to False.
        
        Raises:
        Returns:
        '''

        return BeautifulSoup(html.unescape(requests.get(url).text), "html.parser")

    def get_category_list(self) -> list[str]:
        '''Method Description.
        Description details here (if needed).
        
        Args:
            name (type): Description. Default to False.
        
        Raises:
        Returns:
        '''

        page = self._get_html_page(self.base_url)
        category_list: list = []

        category_div: str = page.find('div', class_="side_categories").find(
            'ul', class_="nav-list"
        ).find('li').find('ul')

        for category in category_div.find_all('a'):
            category_list.append(category['href'])

        return category_list

    def get_book_list(self, page_url, multi_page: bool = False) -> list[str]:
        '''Method Description.
        Description details here (if needed).
        
        Args:
            name (type): Description. Default to False.
        
        Raises:
        Returns:
            list[dict[str, str]: Liste containing 
                a dictionary for each book found with its data and data url
        '''
        page = self._get_html_page(f'{self.base_url}{page_url}')
        book_list: list = []

        for book_div in page.find_all('article', class_="product_pod"):
            book_list.append(book_div.find('a')['href'][9:])

        try:
            if multi_page:
                next_page__url = f"{page_url[:-11]}{page.find('li', class_='next').find('a')['href']}"
            else:
                next_page__url = f"{page_url[:-10]}{page.find('li', class_='next').find('a')['href']}"
            for item in self.get_book_list(next_page__url, True):
                book_list.append(item)
        except:
            return book_list

        return book_list

    def get_book_data(self, page_url, category_url) -> dict[str, str]:
        '''Method Description.
        Description details here (if needed).
        
        Args:
            name (type): Description. Default to False.
        
        Raises:
        Returns:
        '''
        page = self._get_html_page(f'{self.base_url}catalogue/{page_url}')

        try:
            product_description = (
                page.find('div', id="product_description").find_next_sibling('p').text
            )
        except:
            product_description = None

        return {
            'title': page.find('h1').text,
            'product_page_url': page_url,
            'universal_product_code': page.find('th', text="UPC")
            .find_next_sibling('td')
            .text,
            'price_including_tax': page.find('th', text="Price (incl. tax)")
            .find_next_sibling('td')
            .text,
            'price_excluding_tax': page.find('th', text="Price (excl. tax)")
            .find_next_sibling('td')
            .text,
            'number_available': page.find('th', text="Availability")
            .find_next_sibling('td')
            .text,
            'product_description': product_description,
            'category': page.find('a', href=f'../{category_url[10:]}').text,
            'review_rating': page.find('p', class_="star-rating")['class'][1],
            'image_url': page.find('img')['src'][6:],
        }

    def download_file(self, image_url: str) -> None:
        '''Method Description.
        Description details here (if needed).
        
        Args:
            name (type): Description. Default to False.
        
        Raises:
        Returns:
        '''

        urllib.request.urlretrieve(
            f'{getenv("URL")}{image_url}', self.images_directory / image_url[19:]
        )

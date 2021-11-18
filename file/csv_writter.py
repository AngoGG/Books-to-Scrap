#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2021-11-18
@note    0.0.1 (2021-11-18) : Init file
'''
from __future__ import annotations

from csv import DictWriter
from os import getenv
from pathlib import Path


class CsvWritter:
    '''.
    Description details here (if needed).
    
    Attributes:
        name (type): Description. Default to False.
    '''

    def __init__(self) -> None:
        '''Constructor'''

        self.csv_directory: Path = Path(__file__).resolve().parent.parent / getenv(
            "CSV_DIR"
        )
        self.csv_directory.mkdir(parents=False, exist_ok=True)

    def write(self, books_data: list[dict[str, str]]) -> None:
        '''Method Description.
        Description details here (if needed).
        
        Args:
            name (type): Description. Default to False.
        
        Raises:
        Returns:
        '''

        csv_path: Path = Path(f"{self.csv_directory}/{books_data[0]['category']}.csv")

        with csv_path.open('w', encoding='UTF-8',) as csv_file:
            fieldnames = [
                'title',
                'product_page_url',
                'universal_product_code',
                'price_including_tax',
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url',
            ]
            list_item_csv = DictWriter(
                csv_file, delimiter='|', lineterminator='\n', fieldnames=fieldnames
            )
            list_item_csv.writeheader()

            for data in books_data:
                list_item_csv.writerow(data)


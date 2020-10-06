from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from bs4 import BeautifulSoup
from functional import seq

from roam import roam_date


class Color(Enum):
    """
    Probably most hacky part of this. Logic is that the colors are represented by images with the given index
    """
    BLUE = 1
    RED = 2
    YELLOW = 3
    GREEN = 4


@dataclass
class Highlight:
    book: str
    text: str
    note: str
    link: str
    page: str
    date: datetime
    color: Color

    def as_roam_markdown(self):
        return seq(
            f' - {self.text}',
            f'   - {self.note}' if self.note else None,
            f'   - [{self.book}: {self.page}]({self.link})',
            f'   - date::[[{roam_date(self.date)}]]',
            f'   - color::#{self.color.name.lower()}'
        ).filter(lambda it: it is not None).make_string('\n')

    def as_anki_csv_row(self):
        soup = BeautifulSoup()
        link = soup.new_tag('a', href=self.link, string=f'{self.book}: {self.page}')

        return [self.text, self.note, link, str(self.date.date()), self.color.name.lower()]

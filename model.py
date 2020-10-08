from dataclasses import dataclass
from datetime import date
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
    date: date
    color: Color

    @property
    def markdown_link(self):
        return f'[{self.book}: {self.page}]({self.link})'

    @property
    def color_attribute(self):
        return f'color::#{self.color.name.lower()}'

    @property
    def date_attribute(self):
        return f'date::[[{roam_date(self.date)}]]'

    def as_roam_block_hierarchy(self):
        return {
            self.text: ([{self.note: []}] if self.note else []) + [
                {self.markdown_link: []},
                {self.date_attribute: []},
                {self.color_attribute: []},
            ]
        }

    def as_roam_markdown(self):
        return seq(
            f' - {self.text}',
            f'   - {self.note}' if self.note else None,
            f'   - {self.markdown_link}',
            f'   - {self.date_attribute}',
            f'   - {self.color_attribute}'
        ).filter(lambda it: it is not None).make_string('\n')

    def as_anki_csv_row(self):
        soup = BeautifulSoup()
        link = soup.new_tag('a', href=self.link, string=f'{self.book}: {self.page}')

        return [self.text, self.note, link, str(self.date), self.color.name.lower()]

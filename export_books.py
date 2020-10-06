import csv
from datetime import datetime
from sys import stdout
from typing import IO

import click
from bs4 import BeautifulSoup, Tag
from functional import seq

from model import Highlight, Color


def save_md(file: IO, highlights: seq):
    file.write(highlights.map(lambda it: it.as_roam_markdown()).make_string('\n'))


def save_csv(file, highlights: seq):
    writer = csv.writer(file)
    writer.writerows(highlights.map(lambda it: it.as_anki_csv_row()))


save_map = {'md': save_md, 'csv': save_csv}


@click.command()
@click.argument('file', type=click.File())
@click.option('-b', '--book-name', required=True, help='Book name, would be appended to the source reference')
@click.option('-o', '--output', default=stdout, help="Output file", type=click.File(mode="w"))
@click.option('-t', '--export-type', default='md', type=click.Choice(save_map.keys()))
def extract_highlights(file, book_name, output, export_type):
    highlights = find_highlights(file, book_name)

    save_map[export_type](output, highlights)


def find_highlights(file, book_name: str):
    """
    The extraction is based on the structure of the HTML file the export from Google Docs would give you for the
    document containing the notes. 1 cell table container, inside of which there is another table that contains cells
    for Image, Highlight, Note and Date.
    """
    soup = BeautifulSoup(file.read(), 'html.parser')
    containers = soup.find_all(rowspan=1, colspan=1)
    return (seq(containers)
            .map(lambda tag: tag.find_all(rowspan=1, colspan=1))
            .filter(lambda quote_tags: len(quote_tags) != 0)
            .map(lambda tags: parse_highlight(*tags, book=book_name))
            .filter(lambda it: it is not None))


def parse_color(color_container: Tag) -> Color:
    color_tag: Tag = color_container.find('img')

    name_color_map = {f'images/image{color.value}.png': color for color in Color}

    return name_color_map[color_tag['src']]


def parse_highlight(color_container, quote, link, book):
    try:
        text, *note, date = quote.find_all('span')
        link_tag: Tag = link.find('a')
        return Highlight(book,
                         text.get_text(),
                         extract_note(note),
                         link_tag['href'],
                         link_tag.string,
                         datetime.strptime(date.get_text(), "%B %d, %Y"),
                         parse_color(color_container))
    except Exception as e:
        print(quote, e)
        return None


def extract_note(note_tags):
    try:
        _, note_tag, _ = note_tags
        return note_tag.get_text()
    except:
        return ""


if __name__ == '__main__':
    extract_highlights()

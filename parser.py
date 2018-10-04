import csv
from sys import stdout

import click
from bs4 import BeautifulSoup, Tag
from functional import seq


@click.command()
@click.argument('file', type=click.File())
@click.option('-b', '--book-name', default="This Book", help='Book name, would be appended to the source reference')
@click.option('-o', '--output', default=stdout, help="Output file", type=click.File(mode="w"))
def extract_highlights(file, book_name, output):
    save(output, find_highlights(file, book_name))


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
            .map(lambda tags: quote_to_row(*tags, book=book_name)))


def save(file, highlights):
    writer = csv.writer(file)
    writer.writerows(highlights)


def quote_to_row(_, quote, link, book):
    try:
        text, *note, date = quote.find_all('span')
        link_tag: Tag = link.find('a')
        link_tag.string = f"{book}: {link_tag.string}"
        return [text.get_text(), extract_note(note), link_tag, date.get_text()]
    except Exception as e:
        print(quote, e)
        return []


def extract_note(note_tags):
    try:
        _, note_tag, _ = note_tags
        return note_tag.get_text()
    except:
        return ""


if __name__ == '__main__':
    extract_highlights()

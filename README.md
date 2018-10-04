# Google Books highlights and notes extractor
A script to extract highlights and notes from Google Books highlight document in Google Drive to CSV.

**Why**. The highlights document is ok to read, but if you want to use the highlights/notes elsewhere, there is no way for you to do this besides manually copying notes one by one.  
My specific use case is adding them to Anki.

This script is going to extract:
* Highlight
* Note (if present)
* Reference to the position in a book where the highlight originates from.
* Date when the highlight was made. 

Each of those are placed in the separate column in resulting CSV file.

### How to use this:

1. Go to the Google Document created by the Google Books with highlights for the book you're interested in;
1. Download it as HTML;
1. Uncompress the archive that you got on the previous step;
1. Install dependencies if any are missing (see requirements.txt)
1. Run parser.py with the HTML file you got after unpacking the archive as an input. 
E.g. `python parser.py /path/to/file.html -o output.csv`

Some other options:
```
Usage: parser.py [OPTIONS] FILE

Options:
  -b, --book-name TEXT   Book name, would be appended to the source reference
  -o, --output FILENAME  Output file
  --help                 Show this message and exit.
```
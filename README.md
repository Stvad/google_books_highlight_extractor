# Google Books highlights and notes extractor
A script to extract highlights and notes from Google Books highlight document in Google Drive.

**Why**. The highlights document is ok to read, but if you want to use the highlights/notes elsewhere, there is no way for you to do this besides manually copying notes one by one.  
My specific use case is adding them to RoamResearch or Anki.

This script is going to extract:
* Highlight
* Note (if present)
* Reference to the position in a book where the highlight originates from.
* Date when the highlight was made. 
* Highlight color


### How to use this:

1. Go to the Google Document created by the Google Books with highlights for the book you're interested in;
1. Download it as HTML;
1. Uncompress the archive that you got on the previous step;
1. Install dependencies if any are missing (see requirements.txt)
1. Run parser.py with the HTML file you got after unpacking the archive as an input. E.g: 
    * Markdown `python export_books.py local /path/to/file.html -o output.md -b "Book name" --since yesterday`
    * Roam Graph `python export_books.py roam /path/to/file.html -b "Book name" --since yesterday --graph stvad-api --api-key <key> --graph-token <token>` 


#### Output formats

This script supports the following output formats:

1. **Markdown** - store output to local Markdown file. Formatted to be pasted in Roam
1. **CSV** - store output to local CSV file. Structured in a way that it's easy to import into Anki
1. **Roam Graph** - this method uses Roam API to add highlights directly to the book's page in your Roam Graph (You'd need API token to use this)

**Full options:** 
```
Usage: export_books.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  local  Output results locally
  roam   Store highlights to a Roam Graph

---

Usage: export_books.py local [OPTIONS] FILE

  Output results locally

Options:
  -b, --book-name TEXT        Book name, would be appended to the source
                              reference  [required]
  --since TEXT                Starting point to take highlights from (supports
                              natural language)
  -o, --output FILENAME       Output file
  -t, --export-type [md|csv]
  --help                      Show this message and exit.

---

Usage: export_books.py roam [OPTIONS] FILE

  Store highlights to a Roam Graph

Options:
  -b, --book-name TEXT  Book name, would be appended to the source reference
                        [required]
  --since TEXT          Starting point to take highlights from (supports
                        natural language)
  -g, --graph TEXT      The name of the Roam graph to store highlights to
                        [required]
  --api-key TEXT        Roam API key  [required]. Also can be supplied through env variable ROAM_API_KEY
  --graph-token TEXT    Roam Graph token  [required]. Also can be supplied through env variable ROAM_GRAPH_TOKEN.
  --help                Show this message and exit.
```
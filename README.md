
# Zero-Password-Generator

## Description
Zero-Password-Generator is an open-source tool designed to create extensive lists of potential passwords through word mutation techniques. This tool takes user-input words and words scraped from specified URLs, then applies a series of mutations to generate a diverse set of password possibilities.

## Features
- Manual input of seed words.
- Web scraping functionality to gather seed words from specified URLs.
- Extensive word mutations for generating a wide variety of password options.
- Output of mutated words to a text file for use in password testing or other applications.

## How to Use
1. Start the script.
2. Input seed words one at a time. Enter 'x' to finish this step.
3. Input URLs for web scraping. Enter 'x' to finish and proceed with word mutation.
4. Wait for the script to process and output the mutated words into `out.txt`.

## Installation Requirements
- Python 3.x
- Libraries: `requests`, `nltk`, `bs4` (BeautifulSoup), `tqdm`
  Install the required libraries using:
  ```
  pip install requests nltk beautifulsoup4 tqdm
  ```
- Ensure NLTK corpora are downloaded:
  ```
  import nltk
  nltk.download('words')
  nltk.download('punkt')
  ```

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.

## Contribution
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

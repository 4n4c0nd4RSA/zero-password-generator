import requests
import nltk
import random
import string
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

list_limit = 1000000

def scrape_words_from_url(url):
    filtered_words = []
    try:
        page = requests.get(url, verify=True)
        soup = BeautifulSoup(page.content, 'html.parser')
        raw_text = soup.get_text()
        words = raw_text.split()
        filtered_words = [word for word in words if word.lower() not in common_words]
    finally:
        return filtered_words

def mutate_loop(word_list, words_to_extend):
    mutated_words = []
    counter = 0
    if len(word_list) > 1000:
        return mutated_words
    for word in word_list:
        try:
            counter = counter + 1
            if len(mutated_words) > list_limit:
                print(f"List size exceeded word limit. Stopping. {len(set(mutated_words))}")
                return mutated_words
            if counter % 10 == 0 or counter == 1 or counter == len(word_list):
                tqdm.write(f"{counter} / {len(word_list)}") 
            # Add upper and lower case variants of the original word
            mutated_words.extend([word.upper(), word.lower()])
            
            # Replace vowels with numbers
            mutated_word = "".join([c if c not in "aeiouAEIOU" else str(random.randint(0,9)) for c in word])
            mutated_words.append(mutated_word)      
            words_to_extend.append(mutated_word)
            
            # Shuffle letters within the word
            mutated_word = "".join(random.sample(word, len(word)))
            mutated_words.append(mutated_word)        
            words_to_extend.append(mutated_word)
        
            # Add or remove letters from the word
            for i in range(len(word)):
                mutated_word = word[:i] + word[i+1:]
                mutated_words.extend([mutated_word, mutated_word.upper()])
                mutated_word = word[:i] + word[i+1:].upper()
                mutated_words.extend([mutated_word, mutated_word.lower()])
            for i in range(len(word)+1):
                for c in string.ascii_lowercase:
                    mutated_word = word[:i] + c + word[i:]
                    mutated_words.extend([mutated_word, mutated_word.upper()])
                    mutated_word = word[:i] + c.upper() + word[i:]
                    mutated_words.extend([mutated_word, mutated_word.lower()])

            for i in range(len(word_list)):
                for j in range(i+1, len(word_list)):
                    mutated_word = word_list[i] + word_list[j]         
                    words_to_extend.append(mutated_word)
                    mutated_words.extend([mutated_word, mutated_word.upper(), mutated_word.lower()])
                    mutated_word = word_list[j] + word_list[i]             
                    words_to_extend.append(mutated_word)
                    mutated_words.extend([mutated_word, mutated_word.upper(), mutated_word.lower()])
            
            # Add leet text variants of the original word
            leet_map = {
                "a": "4",
                "b": "8",
                "e": "3",
                "g": "9",
                "i": "1",
                "l": "1",
                "o": "0",
                "s": "5",
                "t": "7",
                "z": "2"
            }
            
            leet_word = "".join([leet_map.get(c.lower(), c) for c in word])
            if leet_word not in mutated_words:
                mutated_words.append(leet_word)
                words_to_extend.append(leet_word)
            
            # Add special character variants of the original word
            special_chars = ["!", "@", "#", "$", "%", "^", "&", "*", "-", "_", "+", "=", "?", "~"]
            for i in special_chars:
                mutated_word = word + "".join(i)
                mutated_words.append(mutated_word)       
                words_to_extend.append(mutated_word)
        except Exception as e:
            print("Error in input")      
            if isinstance(e, KeyboardInterrupt):
                raise e
    words_to_extend = set(words_to_extend)
    return mutated_words

def apply_mutations(word_list):

    words_to_extend_1 = []
    mutated_words = []
    mutated_words_1 = mutate_loop(word_list,words_to_extend_1)
    mutated_words_2 = mutate_loop(words_to_extend_1,[])
    if mutated_words_1 is not None and mutated_words_2 is not None:
        mutated_words = mutated_words_1 + mutated_words_2      
    
    return list(set(mutated_words))




nltk.download('words')
nltk.download('punkt')

# get a list of English words from the NLTK corpus
common_words = list(set(nltk.corpus.words.words()))

words_list = []
while True:
    word = input("Enter a word to add to the list (or 'x' to stop adding words): ")
    if word == "x":
        break
    words_list.append(word)
    if len(words_list) > list_limit:
        print("List size exceeded 1 million words. Stopping. B")
        break

url_list = []
while True:
    url = input("Enter a URL to scrape (or 'x' to stop adding URLs): ")
    if url == "x":
        break
    url_list.append(url)

scraped_words = []
if len(url_list) > 0:
    for url in tqdm(url_list, desc="Scraping URLs"):
        scraped_words.extend(scrape_words_from_url(url))
        if len(scraped_words) > list_limit:
            print("List size exceeded 1 million words. Stopping. A")
            break

unique_words = list(set(words_list + scraped_words))

mutated_words = apply_mutations(unique_words)

with open("out.txt", "w", encoding="utf-8") as f:
    for word in tqdm(mutated_words, desc="Writing output"):
        f.write(word + "\n")

# Functions related to data cleaning and word extraction
import re
# Pattern used for regex
word_pattern = r"([A-Za-zÀ-ÿ\u00f1\u00d1\d_\@://\.-]+)"
word_pattern_no_symbols = r"([A-Za-zÀ-ÿ\u00f1\u00d1\d_]+)"
word_pattern_test = r"[(\w@/:)+\.]+"
word_pattern_email = r"[A-Za-zÀ-ÿ\u00f1\u00d1\d_\@://-]+\.[A-Za-zÀ-ÿ\u00f1\u00d1\d_\@://-]+"
tag_pattern = r"<.*?>"
global_stopwords = ['a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'e', 'el', 'en', 'entre', 'hacia', 'hasta',
                    'ni', 'la', 'le', 'lo', 'los', 'las', 'o', 'para', 'pero', 'por', 'que', 'se', 'segun', 'sin', 'so', 'sobre',
                    'tras', 'u', 'un', 'una', 'unas', 'uno', 'unos', 'y']

# Start of functions

# Normalizes accents
def normalize_word(word):
    word = word.lower()
    word = word.replace('á', 'a')
    word = word.replace('é', 'e')
    word = word.replace('í', 'i')
    word = word.replace('ó', 'o')
    word = word.replace('ú', 'u')
    word = word.replace('ü', 'u')

    return word

def insert_glob_dict(word,globalDict):
    if word in globalDict:
        globalDict[word] += 1
    else:
        globalDict[word] = 1
    return

# Retrieves every word in a document that is not a xml tag or in the stopwords list
def clean_xml(lines,stopwords,globalDict):

    words_dict = {}
    # For now it grabs words separated with "-" as one word
    lines = re.sub(tag_pattern,"",lines)
    # TODO: Define a definitive regex expression
    words = re.findall(word_pattern_no_symbols,lines)
    total_word_count = 0
    for word in words:
        word = normalize_word(word)
        if word not in stopwords:
            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1
            insert_glob_dict(word,globalDict)
            total_word_count += 1
    print(f'Total count {total_word_count}')
    print(f'Number of different words {len(words_dict)}')
    return words_dict

# Retrieves stopwords in a document and returns an array containing every stopword
def load_stopwords(lines_stop):
    stopwords = re.findall(word_pattern,lines_stop)
    for stopword in stopwords:
        if stopword not in global_stopwords:
            global_stopwords.append(stopword)
    return global_stopwords


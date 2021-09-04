# Functions related to data cleaning and word extraction

# Imports
import re
import sys
from utils import open_file, load_directory_files
from Structures.Collection import Collection
from Structures.Posting import Posting
from Structures.Term import Term
from Structures.Document import Document

# Package setup
sys.path.insert(0, './Structures')

# Pattern used for regex
word_pattern_no_symbols = r"([A-Za-zÀ-ÿ\u00f1\u00d1\d_]+)"
word_pattern_test = r"[(\w@/:)+\.]+"
tag_pattern = r"<.*?>"
global_stopwords = ['a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'e', 'el', 'en', 'entre', 'hacia',
                    'hasta',
                    'ni', 'la', 'le', 'lo', 'los', 'las', 'o', 'para', 'pero', 'por', 'que', 'se', 'segun', 'sin', 'so',
                    'sobre',
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
def clean_xml(lines, stopwords, collection, doc_id):
    lines = re.sub(tag_pattern, "", lines)
    words = re.findall(word_pattern_no_symbols, lines)
    total_word_count = 0
    for word in words:
        word = normalize_word(word)
        if word not in stopwords:
            collection.insert_term(word,doc_id)
            total_word_count += 1
    collection.documents[str(doc_id)].size = total_word_count
    return


# Retrieves stopwords in a document and returns an array containing every stopword
def load_stopwords(lines_stop):
    stopwords = re.findall(word_pattern_no_symbols, lines_stop)
    for stopword in stopwords:
        if stopword not in global_stopwords:
            global_stopwords.append(stopword)
    return global_stopwords


# Test function for cleaning functions
def start_indexing(collection_path, stopwords_path, target_path):
    path = stopwords_path
    file = open_file(path)
    stopwords = load_stopwords(file.read())
    documents = load_directory_files(collection_path)
    if len(documents) == 0:
        print("No existen documentos para indexar en este directorio")
        return
    collection = Collection(collection_path, stopwords_path)
    doc_id_counter = 1
    for document in documents:
        collection.documents[str(doc_id_counter)] = Document(document)
        clean_xml(open_file(document).read(), stopwords, collection,doc_id_counter)
        doc_id_counter += 1
    collection.size = len(collection.documents)
    collection.calculate_avr_size()
    print(collection)
    print(len(collection.dictionary))

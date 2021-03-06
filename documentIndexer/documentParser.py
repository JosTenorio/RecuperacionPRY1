# Functions related to data cleaning and word extraction

# Imports
import re
import sys
from shlex import split
import numpy as np
from Structures.Collection import Collection
from Structures.Document import Document
from utils import load_directory_files, open_file, is_path, is_file, normalize_word
from utils import write_index, copy_file

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


# Functions


# Argument validation
def validate_arguments(line):
    try:
        args = split(line)
    except ValueError:
        print("Error: Se han abierto comillas simples sin el respectivo cierre" + ", por favor reintentar")
        return [True, None, None, None]
    if len(args) != 3:
        print("Error: Se esperaban 3 parámetros pero se recibieron " + str(len(args)) + ", por favor reintentar")
        return [True, None, None, None]
    collection_path, stopwords_path, target_path = args
    error = False
    if not is_path(collection_path):
        print("Asegurese de que el directorio de la colección tenga un formato correcto")
        error = True
    if not is_file(stopwords_path):
        print("Asegúrese de que la ruta del archivo de stopwords tenga como objetivo un archivo en formato txt")
        error = True
    if not is_path(target_path):
        print("Asegurese de que el directorio objetivo del índice tenga un formato correcto")
        error = True
    return [error, collection_path, stopwords_path, target_path]


def insert_glob_dict(word, global_dict):
    if word in global_dict:
        global_dict[word] += 1
    else:
        global_dict[word] = 1
    return


# Retrieves every word in a document that is not a xml tag or in the stopwords list
def clean_xml(lines, stopwords, collection, doc_id):
    lines = re.sub(tag_pattern, "", lines)
    words = re.findall(word_pattern_no_symbols, lines)
    total_word_count = 0
    for word in words:
        word = normalize_word(word)
        if word not in stopwords:
            collection.insert_term(word, doc_id)
            total_word_count += 1
    collection.documents[doc_id].size = total_word_count
    return


# Retrieves stopwords in a document and returns an array containing every stopword
def load_stopwords(lines_stop):
    stopwords = re.findall(word_pattern_no_symbols, lines_stop)
    for stopword in stopwords:
        stopword = normalize_word(stopword)
        if stopword not in global_stopwords:
            global_stopwords.append(stopword)
    return global_stopwords


# Test function for cleaning functions
def start_indexing(line):
    args = validate_arguments(line)
    error, collection_path, stopwords_path, target_path = args
    if error:
        return
    path = stopwords_path
    try:
        file_stopwords = open_file(path)
        stopwords = load_stopwords(file_stopwords.read())
        copy_file(stopwords, target_path)
    except FileNotFoundError:
        print("Error: El archivo de stopwords indicado no se puede acceder o copiar,"
              " por favor reintentar")
        return
    documents = load_directory_files(collection_path)
    if len(documents) == 0:
        print("No existen documentos para indexar en este directorio")
        return
    collection = Collection(collection_path, "stopwords.txt")
    doc_id_counter = 1
    for document in documents:
        collection.documents[doc_id_counter] = Document(document)
        clean_xml(open_file(document).read(), stopwords, collection, doc_id_counter)
        doc_id_counter += 1
    collection.size = len(collection.documents)
    collection.calculate_avr_size()
    calc_inv_frequency(collection)
    calc_weight(collection)
    write_index(collection, target_path)


# Function that calculates the inverted document frequency of each term in both the vector based and bm25 models.
def calc_inv_frequency(collection):
    for term in collection.dictionary:
        term_struct = collection.dictionary[term]
        term_struct.inv_frequency_vec = np.log2(collection.size / len(term_struct.postings))
        if len(term_struct.postings.keys()) > (collection.size / 2):
            term_struct.inv_frequency_bm5 = 0
        else:
            term_struct.inv_frequency_bm5 = np.log2((collection.size - len(term_struct.postings.keys()) + 0.5) /
                                                    (len(term_struct.postings.keys()) + 0.5))


# Function that adds the weights of each term in the vector based model, it also calculates the norm of each document
def calc_weight(collection):
    collection_size = collection.size
    for docid in collection.documents:
        total_doc_weight = 0
        for term in collection.dictionary:
            term_struct = collection.dictionary[term]
            if docid in term_struct.postings:
                weight = np.log2((1 + term_struct.postings[docid].frequency)) * np.log2(
                    collection_size / len(term_struct.postings))
                term_struct.postings[docid].weight_vec = weight
                total_doc_weight += np.square(weight)
        norm = np.sqrt(total_doc_weight)
        collection.documents[docid].norm = norm

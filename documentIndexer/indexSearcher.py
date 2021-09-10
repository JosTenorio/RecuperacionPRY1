# Functions related to index querying

# Imports
import sys
from shlex import split
from os import path
from utils import load_index, normalize_word, open_file
from documentParser import load_stopwords
import operator
import numpy as np

# Package setup
sys.path.insert(0, './Structures')

# Global parameters for bm25 search
k = 1.2
b = 0.75


# Parameter validation
def validate_parameters(line):
    try:
        params = split(line)
    except ValueError as exc:
        print(exc.args)
        raise ValueError("Error: Se han abierto comillas simples sin el respectivo cierre" + ", por favor reintentar")
    if len(params) < 5:
        raise ValueError("Error: Se esperaban al menos 5 parámetros pero se recibieron " + str(len(params))
                         + ", por favor reintentar")
    if params[1] != "vec" and params[1] != "bm25":
        raise ValueError("Error: El tipo de la búsqueda debe ser 'vec' o 'bm25' pero se recibió " +
                         params[1] + ", por favor reintentar")
    if not path.isdir(params[0]):
        raise ValueError("Error: El directorio de índice especificado no existe o no se ha podido abrir" +
                         ", por favor reintentar")
    try:
        num_docs = int(params[3])
    except ValueError:
        raise ValueError("Error: No se ha podido leer un valor numérico entero para la cantidad de documenos a" +
                         " mostrar en el escalafón, por favor reintentar")
    if num_docs < 1:
        raise ValueError("Error: La cantidad de documentos a mostrar en el escalafón debe ser por lo menos uno" +
                         ", por favor reintentar")
    query = [normalize_word(q) for q in params[4:]]
    return {"index_path": params[0], "type": params[1], "result_prefix": params[2], "num_docs": num_docs,
            "query": query}


def vector_query(collection, query):
    print("El método que hará mi cafetalero favorito")


def bm25_query(collection, query):
    similitudes = {}
    for word in query:
        if word in collection.dictionary:
            term = collection.dictionary[word]
            for posting in term.postings.values():
                doc = collection.documents[posting.doc_id]
                similitude = term.inv_frequency_bm5 * ((posting.frequency * (k + 1)) /
                                                       (posting.frequency + k * (
                                                                   1 - b + b * (doc.size / collection.avr_length))))
                if posting.doc_id not in similitudes:
                    similitudes[posting.doc_id] = similitude
                else:
                    similitudes[posting.doc_id] += similitude
    return similitudes


# Entry point function
def query_index(line):
    try:
        params = validate_parameters(line)
    except ValueError as exc:
        print(exc.args[0])
        return
    try:
        collection = load_index(params["index_path"])
    except FileNotFoundError:
        print("Error: El directorio de indíce especificado no contiene ningún índice o este no se puede acceder,"
              " por favor reintentar")
        return
    try:
        stopwords_path = params["index_path"] + "/" + collection.stopwords
        stopwords_file = open_file(stopwords_path)
        stopwords = load_stopwords(stopwords_file.read())

    except FileNotFoundError:
        print("Error: El directorio de indíce especificado no contiene ningún archivo de stopwords,"
              "por favor colocar de nuevo el archivo o reindexar la colección")
        return
    query = clean_query(params["query"], stopwords)
    similitudes = {}
    if params["type"] == "vec":
        similitudes = vector_query(collection, query)
    else:
        similitudes = bm25_query(collection, query)
    ranking = sorted(similitudes.items(), key=operator.itemgetter(1), reverse=True)


def clean_query(query, stopwords):
    cleaned_query = []
    for word in query:
        cleaned_word = normalize_word(word)
        if cleaned_word not in stopwords:
            cleaned_query.append(cleaned_word)
    return cleaned_query

# Functions related to index querying

# Imports
import sys
from shlex import split
from os import path
from collections import Counter
import operator
import numpy as np
from datetime import datetime
import numpy as np

from utils import load_index, normalize_word, open_file,remove_tags
from documentParser import load_stopwords
from Structures.Term_query import Term_query

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

# Function in charge of calculating the similitude of every document based in a query
def vector_query(collection, query):
    similitudes = {}
    query_dict, query_norm = calc_query_weight(query,collection)
    for word in query_dict:
        if word in collection.dictionary:
            term = collection.dictionary[word]
            for posting in term.postings.values():
                doc = collection.documents[posting.doc_id]
                similitude = (query_dict[word].weight * posting.weight_vec)/(doc.norm*query_norm)
                if posting.doc_id not in similitudes:
                    similitudes[posting.doc_id] = similitude
                else:
                    similitudes[posting.doc_id] += similitude
    return similitudes


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

    write_html_ranking(ranking,collection,params["query"],params["result_prefix"],params["num_docs"],params["index_path"])

# Function that cleans and normalizes the input given in a query
def clean_query(query, stopwords):
    cleaned_query = []
    for word in query:
        cleaned_word = normalize_word(word)
        if cleaned_word not in stopwords:
            cleaned_query.append(cleaned_word)
        return cleaned_query
# Function that calculates the weight of every term in a query
def calc_query_weight(query,collection):
    query = Counter(query)
    sum_for_norm = 0
    query_dictionary = {}
    for term in query.keys():
        if term in collection.dictionary:
            weight = np.log2(1+query[term])*np.log2(collection.size/len(collection.dictionary[term].postings))
            sum_for_norm += np.square(weight)
            term_info = Term_query(term, query[term], weight)
            query_dictionary[term] = term_info
    norm = np.sqrt(sum_for_norm)
    return [query_dictionary, norm]
# Function that saves an html file containing all the information used in the query and the ranking obtained.      
def write_html_ranking(ranking,collection,original_query,prefix,numdocs,index_path):
    filename = index_path+f"/{prefix}.html"
    html_file = open(filename,"w",encoding="UTF-8")
    original_query = ' '.join([str(elem) for elem in original_query])
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    html_text = f"""
    <!DOCTYPE html> 
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="../resources/style.css" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
        href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap"
        rel="stylesheet"
        />
    </head>
    <header>
        <h1 class="title">Resultado de la búsqueda de documentos</h1>
    </header>
    <body>
        <div>
            <div>
                <div class="label-box">
                <h2>Consulta realizada:</h2>
                </div>
                <div class="query-box">
                <h2>{original_query}</h2>
                </div>
            </div>
            <div style="clear: left">
                <div class="label-box">
                <h2>Hora de la consulta:</h2>
                </div>
                <div class="query-box">
                <h2>{date}</h2>
                </div>
            </div>
        </div>
    <div>

    """
    html_file.write(html_text)
    for count, result in enumerate(ranking,1):
        if count>numdocs:
            break
        doc_path = collection.documents[result[0]].address
        doc_file = open_file(doc_path)
        doc_Text = remove_tags(doc_file.read())
        ranking_text= f"""
        <div style="clear:left">
            <div>
                <div class="ranking-box">
                <h3>Posición en el ranking:</h3>
                </div>
                <div class="query-box">
                <h3>{count}</h3>
                </div>
            </div>
             <div>
                <div class="ranking-box">
                <h3>Similitud:</h3>
                </div>
                <div class="query-box">
                <h3>{result[1]}</h3>
                </div>
            </div>
            <div>
              <div class="ranking-box">
                <h3>Id del documento:</h3>
                </div>
                <div class="query-box">
                <h3>{result[0]}</h3>
                </div>
            </div>
            <div>
                <div class="ranking-box">
                <h3>Directorio del documento:</h3>
                </div>
                <div class="query-box">
                <a href={doc_path}> <h3>{doc_path}</h3> </a>
                </div>
            </div>
            <div style="clear:left;margin-left:40px;width:70%">
            <p>{doc_Text[:200]}</p>
            </div>
        </div>
        """
        html_file.write(ranking_text)
    html_file.write("   </div> </body> </html>")
    html_file.close()
    
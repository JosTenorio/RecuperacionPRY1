# Functions related to index inspection

# Imports
import sys
from shlex import split
from os import path
from utils import load_index, normalize_word

# Package setup
sys.path.insert(0, './Structures')


# Functions

# Parameter validation
def validate_parameters(line):
    try:
        params = split(line)
    except ValueError as exc:
        print(exc.args)
        raise ValueError("Error: Se han abierto comillas simples sin el respectivo cierre" + ", por favor reintentar")
    if len(params) != 3:
        raise ValueError(
            "Error: Se esperaban 3 parámetros pero se recibieron " + str(len(params)) + ", por favor reintentar")
    if params[1] != "ter" and params[1] != "doc":
        raise ValueError("Error: El tipo de la inspección debe 'ter' o 'doc' pero se recibió " + params[
            1] + ", por favor reintentar")
    if not path.isdir(params[0]):
        raise ValueError(
            "Error: El directorio de índice especificado no existe o no se ha podido abrir" + ", por favor reintentar")
    return {"index_path": params[0], "type": params[1], "data_path": params[2]}


# Document inspection
def inspect_doc(collection, doc_path):
    real_doc_path = path.normcase(collection.address + "\\" + doc_path)
    search_result = [(k, v) for k, v in collection.documents.items() if path.normcase(v.address) == real_doc_path]
    if not search_result:
        print("No se encontró la entrada de la colección correspondiente a la ruta relativa dada, por favor reintentar")
        return
    else:
        doc_id, doc = search_result[0]
        print("Detalles del documento: " + str(path.normcase(doc_path)) + "\n\nId: " + str(doc_id) + "\nLongitud: "
              + str(doc.size) + "\nNorma: " + str(doc.norm))


# Term inspection and display
def inspect_term(collection, term_spelling):
    if term_spelling not in collection.dictionary:
        print("No se encontró la entrada de la colección correspondiente al término dado, por favor reintentar")
        return
    term = collection.dictionary[normalize_word(term_spelling)]
    print("Detalles del término '" + term_spelling + "': \n\nDocumentos en los que aparece (ni): " +
          str(len(term.postings.keys())) + "\nIDF vectorial: " + str(term.inv_frequency_vec) + "\nIDF BM25: "
          + str(term.inv_frequency_bm5))
    print("Postings (id del documento, frecuencia en el documento, peso vectorial): ")
    for k, v in term.postings.items():
        print("(%s, %s, %s)" % (str(k), str(v.frequency), str(v.weight_vec)))


# Entry point function
def inspect_index(line):
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
    if params["type"] == "ter":
        inspect_term(collection, params["data_path"])
    else:
        inspect_doc(collection, params["data_path"])

# Functions related to index inspection

# Imports
import sys
from shlex import split
from os import path
from utils import load_index

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
    # dic_item = [k for k, v in collection.documents.items() if k.address == doc_path][0]
    print(doc_path)


# Term inspection
def inspect_term(collection, term):
    print(term)


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
        print("Error: El directorio de indíce especificado no contiene ningún índice o este no se puede acceder, por favor reintentar")
        return
    if params["type"] == "ter":
        inspect_term(collection, params["data_path"])
    else:
        inspect_doc(collection, params["data_path"])

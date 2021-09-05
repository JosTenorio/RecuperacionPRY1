from shlex import split


def validate_parameters(line):
    try:
        params = split(line)
    except ValueError as exc:
        print(exc.args)
        raise ValueError("Error: Se han abierto comillas simples sin el respectivo cierre" + ", por favor reintentar")
    if len(params) != 3:
        raise ValueError("Error: Se esperaban 3 parámetros pero se recibieron " + str(len(params)) + ", por favor reintentar")
    if params[1] != "ter" and params[1] != "doc":
        raise ValueError("Error: El tipo de la inspección debe 'ter' o 'doc' pero se recibió " + params[1] + ", por favor reintentar")
    # TODO validate parameters
    print (params)
    return {"index_path": params[0], "type": params[1], "data_path": params[2]}


def inspect_doc(collection, doc_path):
    #dic_item = [k for k, v in collection.documents.items() if k.address == doc_path][0]


    print(doc_path)

#C:\Users\Personal\Desktop\RecuperacionPRY1\Archivos de prueba\xml-es

def inspect_term(collection, term):
    print(term)


def inspect_index(line):
    try:
        params = validate_parameters(line)
    except ValueError as exc:
        print(exc.args[0])
        return
    if params["type"] == "ter":
        inspect_term(None, params["data_path"])
    else:
        inspect_doc(None, params["data_path"])

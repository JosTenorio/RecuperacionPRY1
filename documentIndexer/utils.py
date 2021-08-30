import glob
import time
import re
from documentParser import load_stopwords,clean_xml
regex_paths= r'[A-z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]*'
regex_files = r'[a-zA-Z]:[\\\/](?:[a-zA-Z0-9]+[\\\/])*([a-zA-Z0-9]+\.txt)'

def is_path(path):
    print(path)
    return bool(re.match(regex_paths,path))
def is_file(path):
    return bool(re.match(regex_files,path))
def open_file(path):
    try:
        file = open(path, encoding="utf-8")
        return file
    except UnicodeDecodeError:
        print(
            "Los archivos deben estar en formato utf-8, se seguirá la ejecución pero puede que los resultados se vean afectados")
        file = open(path)
        return file
    except FileNotFoundError:
        return 0


def load_directory_files(path):
    return glob.glob(path+"/**/*.xml",recursive=True)

# Test function for cleaning functions
def start_indexing(collection_path,stopwords_path,target_path):
    path=stopwords_path
    file = open_file(path)
    stopwords = load_stopwords(file.read())
    documents = load_directory_files(collection_path)
    if len(documents) == 0:
        print("No existen documentos para indexar en este directorio")
        return
    dics = []
    glob_dict = {}
    for document in documents:
        dics.append(clean_xml(open_file(document).read(),stopwords,glob_dict))
    print(len(glob_dict))
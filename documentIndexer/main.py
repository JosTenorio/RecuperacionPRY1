from documentParser import clean_xml,load_stopwords
import glob
import time
from multiprocessing import Pool
# Receives a path to a file and returns the content if it match certain criteria
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


# Standard menu function
def menu():
    while True:
        print("Menú \n0 -> Salir")
        action = input("Acción a realizar: ")
        if(action=="0"):
            break

# Test function for cleaning functions
def test_clean_xml():
    path="D:\\Development\\RecuperacionPRY1\\documentIndexer\\stopWords\\stopWords1.txt"
    file = open_file(path)
    stopwords = load_stopwords(file.read())
    documents = load_directory_files("D:\\Development\\RecuperacionPRY1\\Archivos de prueba\\xml-es")
    if len(documents) == 0:
        print("No existen documentos para indexar en este directorio")
        return
    dics = []
    glob_dict = {}
    inicio = time.time()
    for document in documents:
        dics.append(clean_xml(open_file(document).read(),stopwords,glob_dict))

   
    print(f'Duración fue de {time.time()-inicio}')
    print(len(glob_dict))

if __name__ == '__main__':

     test_clean_xml()
    # menu()


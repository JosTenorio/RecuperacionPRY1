from documentParser import clean_xml,load_stopwords

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

def get_files_in_folder(directory):
    # TODO: Todo xd
    pass
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
    path = "D:\\Development\\RecuperacionPRY1\\Archivos de prueba\\xml-es\\apx-authors.xml"
    file = open_file(path)
    if file==0:
        print("No se encontró el archivo")
        return
    words = clean_xml(file.read(),stopwords)

if __name__ == '__main__':

    test_clean_xml()
    # menu()


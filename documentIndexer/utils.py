import glob
import time
import re
import sys
import pickle
# Package setup
sys.path.insert(0, './Structures')

# Utility REGEX
regex_paths= r'[A-z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]*'
regex_files = r'[a-zA-Z]:[\\\/](?:[a-zA-Z0-9]+[\\\/])*([a-zA-Z0-9]+\.txt)'

def is_path(path):
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

def write_index(collection,destination):
    f = open(destination+"file.pkl", "wb")
    pickle.dump(collection,f)
    f.close()

import glob
import re
import sys
import pickle

# Package setup
sys.path.insert(0, './Structures')

# Utility REGEX
regex_paths = r'[A-z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]*'
regex_files = r'[a-zA-Z]:[\\\/](?:[a-zA-Z0-9]+[\\\/])*([a-zA-Z0-9]+\.txt)'
tag_pattern = r"<.*?>"


# Normalizes accents
def normalize_word(word):
    word = word.lower()
    word = word.replace('á', 'a')
    word = word.replace('é', 'e')
    word = word.replace('í', 'i')
    word = word.replace('ó', 'o')
    word = word.replace('ú', 'u')
    word = word.replace('ü', 'u')

    return word

# Validation for paths
def is_path(path):
    return bool(re.match(regex_paths, path))

# Validation for files
def is_file(path):
    return bool(re.match(regex_files, path))

# Fucntion that returns a file given a path
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
        raise FileNotFoundError("No se encontró el archivo")


def load_directory_files(path):
    return glob.glob(path + "/**/*.xml", recursive=True)


def write_index(collection, destination):
    f = open(destination + "/file.pkl", "wb")
    pickle.dump(collection, f)
    f.close()


# Function that loads a collection from a previously created index
def load_index(location):
    f = open(location + "/file.pkl", "rb")
    index = pickle.load(f)
    f.close()
    return index

# Function that copies a file from one directory to another
def copy_file(content, target):
    f = open(target + "/stopwords.txt", "w", encoding="utf-8")
    for line in content:
        f.write(line + " ")
    f.close()
    return


# Function that receives an xml file and return the raw text without the tags
def remove_tags(text):
    lines = re.sub(tag_pattern, "", text)
    lines = lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    clean_text = ""
    for line in non_empty_lines:
      clean_text += line + "\n"
    return clean_text

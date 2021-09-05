import cmd
from indexInspector import inspect_index

from documentParser import clean_xml, load_stopwords,start_indexing
from utils import load_directory_files, open_file, is_path,is_file


class Terminal(cmd.Cmd):
    prompt = ">>"

    intro = "----------------------------------------------------------------------------------------\n" \
            "Bienvenido a la herramienta de consulta de archivos de texto \n" \
            "La lista de comandos diponibles es: \n" \
            ">>indizar  '[Colección]'  '[Stopwords]' '[Indice]'\n" \
            ">>buscar  '[Indice]'  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]\n" \
            ">>mostrar  '[Indice]'  [Tipo]  '[Dato]'\n" \
            ">>salir\n" \
            "Con '>>help' o '>>?' puede consultar esta lista o algun comando en especifico\n" \
            "Recuerde que las direcciones de archivos se deben digitar entre comillas simples ('')\n" \
            "----------------------------------------------------------------------------------------"

    def do_indizar(self, line):
        """indizar  '[Colección]'  '[Stopwords]' '[Indice]'
        Crea un índice para los archivos del directorio [Colección]"""
        args = line.split()
        if(len(args)<3):
            print("Por ingrese todos los parámetros correctamente")
            return
        collection_path,stopwords_path,target_path = args
        error=False
        if(not is_path(collection_path)):
            print("Asegurese de que el directorio de la colección tenga un formato correcto (No puede contener espacios)")
            error = True
        if(not is_file(stopwords_path)):
            print("Asegúrese de que la ruta del archivo de stopwords tenga como objetivo un archivo en formato txt")
            error = True
        if(not is_path(target_path)):
            print("Asegurese de que el directorio objetivo del índice tenga un formato correcto")
            error = True
        if(error):
            return
        else:
            start_indexing(collection_path,stopwords_path,target_path)




    def do_buscar(self, line):
        """buscar  '[Indice]'  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]
        Realiza la consulta con los paramétros especificados sobre el índice en el directorio [Indice]"""
        print("Comando de busquéda")

    def do_mostrar(self, line):
        """mostrar  '[Indice]'  [Tipo]  '[Dato]'
        Muestra la información guardada en índice en el directorio [Indice]"""
        inspect_index(line)

    def do_salir(self, line):
        """salir
        Termina la ejecución del programa"""
        return True

    def do_help(self, line):
        if len(line.split()) > 0:
            cmd.Cmd.do_help(self, line)
        else:
            print("La lista de comandos diponibles es: \n" \
                  ">>indizar  '[Colección]'  '[Stopwords]' '[Indice]'\n" \
                  ">>buscar  '[Indice]'  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]\n" \
                  ">>mostrar  '[Indice]'  [Tipo]  '[Dato]'\n" \
                  ">>salir\n" \
                  "Con '>>help' o '>>?' puede consultar esta lista o algun comando en especifico\n"\
                  "Recuerde que las direcciones de archivos se deben digitar entre comillas simples ('')\n")

    def do_EOF(self, line):
        return True

    def postloop(self):
        print("Terminando ejecución")

    def default(self, line):
        print("No se reconoce el comando: '" + line.split()[0] + "', por favor intentar de nuevo.")

    def emptyline(self):
        print("Por favor digite alguno de los comandos disponibles.")


if __name__ == '__main__':
    Terminal().cmdloop()
    # Index test comand indizar D:\Development\RecuperacionPRY1\Archivos_de_prueba\xml-es D:\Development\RecuperacionPRY1\documentIndexer\stopWords\stopWords1.txt D:\Development\RecuperacionPRY1\documentIndexer\stopWords

# mostrar 'C:\Users\Personal\Desktop\RecuperacionPRY1\Archivos de prueba\xml-es' doc 'C:\Users\Personal\Desktop\RecuperacionPRY1\Archivos de prueba\xml-es'

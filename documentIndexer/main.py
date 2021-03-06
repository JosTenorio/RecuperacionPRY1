import cmd
from indexInspector import inspect_index
from documentParser import start_indexing
from indexSearcher import query_index


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
        start_indexing(line)

    def do_buscar(self, line):
        """buscar  '[Indice]'  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]
        Realiza la consulta con los paramétros especificados sobre el índice en el directorio [Indice]"""
        query_index(line)

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
            print("La lista de comandos diponibles es: \n"
                  ">>indizar  '[Colección]'  '[Stopwords]' '[Indice]'\n"
                  ">>buscar  '[Indice]'  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]\n"
                  ">>mostrar  '[Indice]'  [Tipo]  '[Dato]'\n"
                  ">>salir\n"
                  "Con '>>help' o '>>?' puede consultar esta lista o algun comando en especifico\n"
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

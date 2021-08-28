import cmd


class Terminal(cmd.Cmd):
    prompt = ">>"

    intro = "-----------------------------------------------------------------------\n" \
            "Bienvenido a la herramienta de consulta de archivos de texto \n" \
            "La lista de comandos diponibles es: \n" \
            ">>indizar  [Colección]  [Stopwords] [Indice]\n" \
            ">>buscar  [Indice]  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]\n" \
            ">>mostrar  [Indice]  [Tipo]  [Dato]\n" \
            ">>salir\n" \
            "Con '>>help' o '>>?' puede consultar esta lista o algun comando en especifico\n" \
            "-----------------------------------------------------------------------"

    def do_indizar(self, person):
        """indizar  [Colección]  [Stopwords] [Indice]
        Greet the named person"""
        print("Comando de indizacion")

    def do_buscar(self, person):
        """buscar  [Indice]  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]
        Greet the named person"""
        print("Comando de busquéda")

    def do_mostrar(self, person):
        """mostrar  [Indice]  [Tipo]  [Dato]
        Greet the named person"""
        print("Comando de inspección")

    def do_salir(self, line):
        """salir
        Termina la ejecución del programa"""
        return True

    def do_help(self, line):
        if len(line.split()) > 0:
            cmd.Cmd.do_help(self, line)
        else:
            print("La lista de comandos diponibles es: \n" \
                  ">>indizar  [Colección]  [Stopwords] [Indice]\n" \
                  ">>buscar  [Indice]  [Tipo]  [Prefijo]  [NumDocs]  [Consulta]\n" \
                  ">>mostrar  [Indice]  [Tipo]  [Dato]\n" \
                  "Con '>>help' o '>>?' puede consultar esta lista o algun comando en especifico\n")

    def do_EOF(self, line):
        return True

    def postloop(self):
        print("Terminando ejecución")


if __name__ == '__main__':
    Terminal().cmdloop()

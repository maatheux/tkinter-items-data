import psycopg2

class AppBD:
    def __init__(self):
        print("Método Construtor")

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="admin", port="5432",
                                               database="project-aula13")
            print("Conectou")
        except(Exception, psycopg2.error) as error:
            if(self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)
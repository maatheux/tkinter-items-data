import tkinter as tk
from tkinter import ttk
import psycopg2
import crud as crud

class principalBD:
    def fLerCampos(self):
        try:
            codigo = int(self.txtCodigo.get())
            nome = self.txtNome.get()
            preco = float(self.txtPreco.get())
            print("Leitura de dados com sucesso!")
        except:
            print("Não foi póssivel ler os dados.")
        return codigo, nome, preco

    def inserirDados(self, codigo, nome, preco):
        try:
            print(codigo, nome, preco)
            self.objBD.abrirConexao()
            cursor = self.objBD.connection.cursor()
            cursor.execute("""INSERT INTO PRODUTO (CODIGO, NOME, PRECO)
                              VALUES (%s,%s,%s)""", (codigo, nome, preco))
            self.objBD.connection.commit()
            count = cursor.rowcount
            print(f"{count} registro inserido com sucesso na tabela PRODUTO")
        except(Exception, psycopg2.Error) as error:
            if(self.objBD.connection):
                print("Falha ao inserir registro na tabela PRODUTO", error)
        finally:
            if(self.objBD.connection):
                cursor.close()
                self.objBD.connection.close()
                print("A conexão com o PostgreSQL foi fechada")

    def fLimparTela(self):
        try:
            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            print("Campos Limpos!")
        except:
            print("Não foi possível limpar os campos")

    def fCadastrarProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            self.inserirDados(codigo, nome, preco)
            self.fLimparTela()
            print("Produto cadastrado com sucesso!")
        except:
            print("Não foi possível fazer o cadastro")

    def atualizarDados(self, codigo, nome, preco):
        try:
            self.objBD.abrirConexao()
            cursor = self.objBD.connection.cursor()
            cursor.execute("""UPDATE public.PRODUTO SET nome= %s, preco= %s WHERE codigo = %s""", (nome, preco, codigo))
            self.objBD.connection.commit()
            count = cursor.rowcount
            print(count, "Registro atualizado com sucesso!")
        except(Exception, psycopg2.Error) as error:
            print("Erro na atualização", error)
        finally:
            if(self.objBD.connection):
                cursor.close()
                self.objBD.connection.close()
                print("A conexão com o PostgreSQL foi fechada")


    def fAtualizarProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            self.atualizarDados(codigo, nome, preco)
            self.fLimparTela()
            print("Produto atualizado com sucesso!")
        except:
            print("Não foi possível fazer a atualização")

    def excluirDados(self, codigo):
        try:
            self.objBD.abrirConexao()
            cursor = self.objBD.connection.cursor()
            cursor.execute("""DELETE FROM public.PRODUTO WHERE codigo = %s""", (codigo, ))
            self.objBD.connection.commit()
            count= cursor.rowcount
            print(count, "registro excluído com sucesso!")
        except(Exception, psycopg2.Error) as error:
            print("Erro na exclusão", error)
        finally:
            cursor.close()
            self.objBD.connection.close()
            print("A conexão com o PostgreSQL foi fechada")

    def fExcluirProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            self.excluirDados(codigo)
            self.fLimparTela()
            print("Produto excluido com sucesso!")
        except:
            print("Não foi possível fazer a exclusão do produto")

    def selecionarDados(self):
        try:
            self.objBD.abrirConexao()
            cursor = self.objBD.connection.cursor()
            print("Selecionando todos os produtos")
            cursor.execute("""SELECT * FROM public.PRODUTO""")
            registros = cursor.fetchall()
            print(registros)
        except(Exception, psycopg2.Error) as error:
            print("Error in select operation", error)
        finally:
            if(self.objBD.connection):
                cursor.close()
                self.objBD.connection.close()
                print("A conexão com o PostgreSQL foi fechada")
        return registros

    def apresentarRegistrosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
            self.txtPreco.insert(0, preco)

    def carregarDadosIniciais(self):
        try:
            registros = self.selecionarDados()
            for item in registros:
                codigo=item[0]
                nome=item[1]
                preco=item[2]
                print("Código = ", codigo)
                print("Nome = ", nome)
                print("Preco = ",preco, "\n")

                self.treeProdutos.insert('', tk.END, values=(codigo, nome, preco))
                print("Dados da base")
        except:
            print("Ainda não existem dados para carregar")

    def __init__(self, win):
        self.objBD = crud.AppBD()

        self.lblCodigo = tk.Label(win, text="Código do produto:")
        self.lblNome = tk.Label(win, text="Nome do produto:")
        self.lblPreco = tk.Label(win, text="Preço do produto")

        self.txtCodigo = tk.Entry(bd=2)
        self.txtNome = tk.Entry(bd=2)
        self.txtPreco = tk.Entry(bd=2)

        self.btnCadastrar = tk.Button(win, text="Cadastrar", command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text="Atualizar", command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(win, text="Excluir", command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text="Limpar", command=self.fLimparTela)

        self.dadosColunas = ("Código", "Nome", "Preço")
        self.treeProdutos = ttk.Treeview(win, columns=self.dadosColunas, show='headings')
        self.verscrbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=self.treeProdutos.yview)
        self.treeProdutos.configure(yscrollcommand=self.verscrbar.set)

        self.treeProdutos.heading("Código", text="Código")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Preço", text="Preço")

        self.treeProdutos.column("Código", minwidth=0, width=100)
        self.treeProdutos.column("Nome", minwidth=0, width=100)
        self.treeProdutos.column("Preço", minwidth=0, width=100)

        self.treeProdutos.pack(padx=10, pady=10)

        self.treeProdutos.bind("<<TreeviewSelect>>", self.apresentarRegistrosSelecionados)

        self.lblCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)

        self.lblPreco.place(x=100, y=130)
        self.txtPreco.place(x=250, y=130)

        self.lblNome.place(x=100, y=90)
        self.txtNome.place(x=250, y=90)

        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)

        self.treeProdutos.place(x=100, y=300)
        self.verscrbar.place(x=405, y=300, height=225)
        self.carregarDadosIniciais()

janela=tk.Tk()
principal = principalBD(janela)
janela.title("Tela de cadastro")
janela.geometry("600x640")
janela.resizable(width=None, height=None)
janela.maxsize(width=600, height=640)
janela.mainloop()
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

# CONECTAR AO BANCO DE DADOS

banco = mysql.connector.connect(
    host='localhost', database='sistema_escolar_proz', 
    user='root', password='')

if banco.is_connected():
    db_info = banco.get_server_info()
    print("Conectado ao servidor MySQL versão:", db_info)
    cursor = banco.cursor()
    cursor.execute('select database();')
    linha = cursor.fetchone()
    print("Conectado ao banco de dados ", linha)
     

def abrir_menu_aluno():  # ABRIR MENU CADASTRO DE ALUNO
    cad_aluno.show()
    
def abrir_menu_prof(): # ABRIR MENU DO PROFESSOR
    cad_prof.show()

def abrir_menu_disc(): # ABRIR MENU DISCIPLINA
    cad_disc.show()

def abrir_menu_mat(): # ABRIR MENU MATRICULA
    cad_mat.show()
    cad_mat.aluno_mat.addItems(["São Paulo","Rio de Janeiro","Minas Gerais","Ceará","Espirito Santo"])


    
def abrir_menuop(): # ABRIR MENU DE MAIS OPÇÕES
    menu_opcao.show()

def cadastro_mat(): # CADASTRO MATRICULA

    cad_mat.aluno_mat.addItems(["São Paulo","Rio de Janeiro","Minas Gerais","Ceará","Espirito Santo"])

    
def cadastro_aluno():   # CADASTRO DOS ALUNOS
    
    linha0 = cad_aluno.codigo_aluno.text()
    linha1 = cad_aluno.nome_aluno.text()
    linha2 = cad_aluno.end_aluno.text()
    linha3 = cad_aluno.cidade_aluno.text()
        
    print("Código: ", linha0)    
    print("Nome do Aluno:", linha1)
    print("Endereço:", linha2)
    print("Cidade:", linha3)
    
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO aluno (codigo_aluno,nome_aluno,endereco_aluno,cidade_aluno) VALUES (%s,%s,%s,%s)"
    dados = (str(linha0), str(linha1), str(linha2), str(linha3))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    cad_aluno.codigo_aluno.setText("") # LIMPAR NOME ALUNO
    cad_aluno.nome_aluno.setText("")  # LIMPAR CAMPO NOME
    cad_aluno.end_aluno.setText("") # LIMPAR CAMPO ENDEREÇO
    cad_aluno.cidade_aluno.setText("") # LIMPAR CAMPO CIDADE
    
def cadastro_prof(): # CADASTRO DOS PROFESSORES
    
    linha1 = cad_prof.nome_prof.text()
    linha2 = cad_prof.end_prof.text()
    linha3 = cad_prof.cidade_prof.text()
            
    print("Nome do Professor:", linha1)
    print("Endereço:", linha2)
    print("Cidade:", linha3)
    
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO professor (nome_prof,end_prof,cidade_prof) VALUES (%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    
    cad_prof.nome_prof.setText("")  # LIMPAR CAMPO NOME
    cad_prof.end_prof.setText("") # LIMPAR CAMPO ENDEREÇO
    cad_prof.cidade_prof.setText("") # LIMPAR CAMPO CIDADE
    
def cadastro_disc(): # CADASTRO DAS DISCIPLINAS
    
    linha1 = cad_disc.nome_disc.text()
    linha2 = cad_disc.curso_disc.text()
    linha3 = cad_disc.n_aulas.text()
            
    print("Nome do Professor:", linha1)
    print("Endereço:", linha2)
    print("Cidade:", linha3)
    
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO disciplina (disc_nome, curso_nome, n_aulas) VALUES (%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    
    cad_disc.nome_disc.setText("")  # LIMPAR CAMPO NOME
    cad_disc.curso_disc.setText("") # LIMPAR CAMPO ENDEREÇO
    cad_disc.n_aulas.setText("") # LIMPAR CAMPO CIDADE
    
    
    
def editar_prof(): # EDIÇÃO PROFESSOR
    global numero_id
    editar = lista_prof.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT codigo_prof FROM professor")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[editar][0]
    cursor.execute(f"SELECT * FROM professor WHERE codigo_prof={str(valor_id)}")
    professor = cursor.fetchall()
    edit_prof.show()
    
    numero_id = valor_id
    
    edit_prof.cod_edit_prof.setText(str(professor[0][0]))
    edit_prof.nome_edit_prof.setText(str(professor[0][1]))
    edit_prof.end_edit_prof.setText(str(professor[0][2]))
    edit_prof.cidade_edit_prof.setText(str(professor[0][3]))

def editar_disc(): # EDIÇÃO DISCIPLINA
    global numero_id
    editar = lista_disc.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT disc_codigo FROM disciplina")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[editar][0]
    cursor.execute(f"SELECT * FROM disciplina WHERE disc_codigo={str(valor_id)}")
    disciplina = cursor.fetchall()
    edit_disc.show()
    
    numero_id = valor_id
    
    edit_disc.cod_edit_disc.setText(str(disciplina[0][0]))
    edit_disc.disc_edit.setText(str(disciplina[0][1]))
    edit_disc.curso_edit.setText(str(disciplina[0][2]))
    edit_disc.aulas_edit.setText(str(disciplina[0][3]))
    
def editar_aluno(): # EDIÇÃO ALUNO
    global numero_id
    editar = lista_alunos.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM aluno")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[editar][0]
    cursor.execute(f"SELECT * FROM aluno WHERE id={str(valor_id)}")
    aluno = cursor.fetchall()
    edit_aluno.show()
    
    numero_id = valor_id
    
    edit_aluno.id_edit_aluno.setText(str(aluno[0][0]))
    edit_aluno.cod_edit_aluno.setText(str(aluno[0][1]))
    edit_aluno.nome_edit_aluno.setText(str(aluno[0][2]))
    edit_aluno.end_edit_aluno.setText(str(aluno[0][3]))
    edit_aluno.cidade_edit_aluno.setText(str(aluno[0][4]))    
    
    
    
def salvar_edit_prof(): # SALVAR EDIÇÃO PROFESSOR
    #pega o numeor do id
    global numero_id
    
    # valor diigitado no campo de edicoes
    codigo = edit_prof.cod_edit_prof.text()
    nome = edit_prof.nome_edit_prof.text()
    endereco = edit_prof.end_edit_prof.text()
    cidade = edit_prof.cidade_edit_prof.text()
    
    # atualizar os dados no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE professor SET codigo_prof = '{}', nome_prof = '{}', end_prof = '{}', cidade_prof = '{}' WHERE codigo_prof = {}" .format(codigo, nome, endereco, cidade, numero_id))
    banco.commit()
    
    #atualizar as janelas
    edit_prof.close()
    lista_prof.close()
    abrir_lista_prof()    

def salvar_edit_disc(): # SALVAR EDIÇÃO DISCIPLINA
    #pega o numeor do id
    global numero_id
    
    # valor diigitado no campo de edicoes
    codigo = edit_disc.cod_edit_disc.text()
    disc2 = edit_disc.disc_edit.text()
    curso = edit_disc.curso_edit.text()
    aulas = edit_disc.aulas_edit.text()
    
    # atualizar os dados no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE disciplina SET disc_codigo = '{}', disc_nome = '{}', curso_nome = '{}', n_aulas = '{}' WHERE disc_codigo = {}" .format(codigo, disc2, curso, aulas, numero_id))
    banco.commit()
    
    #atualizar as janelas
    edit_disc.close()
    lista_disc.close()
    abrir_lista_disc()    
        
def salvar_edit_aluno(): # SALVAR EDIÇÃO DO ALUNO
    #pega o numeor do id
    global numero_id
    
    # valor diigitado no campo de edicoes
    codigo = edit_aluno.cod_edit_aluno.text()
    nome = edit_aluno.nome_edit_aluno.text()
    endereco = edit_aluno.end_edit_aluno.text()
    cidade = edit_aluno.cidade_edit_aluno.text()
    
    # atualizar os dados no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE aluno SET codigo_aluno = '{}', nome_aluno = '{}', endereco_aluno = '{}', cidade_aluno = '{}' WHERE id = {}" .format(codigo, nome, endereco, cidade, numero_id))
    banco.commit()
    
    #atualizar as janelas
    edit_aluno.close()
    lista_alunos.close()
    abrir_lista_alunos()        
      
      
        
def excluir_prof(): # EXCLUIR PROFESSOR
    excluir = lista_prof.tableWidget.currentRow()
    lista_prof.tableWidget.removeRow(excluir)
    
    cursor = banco.cursor()
    cursor.execute("SELECT codigo_prof FROM professor")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[excluir][0]
    cursor.execute(f"DELETE FROM professor WHERE codigo_prof= {str(valor_id)}")
    banco.commit()   # EXCLUIR NO BANCO DE DADOS

def excluir_disc(): # EXCLUIR DISCIPLINA
    excluir = lista_disc.tableWidget.currentRow()
    lista_disc.tableWidget.removeRow(excluir)
    
    cursor = banco.cursor()
    cursor.execute("SELECT disc_codigo FROM disciplina")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[excluir][0]
    cursor.execute(f"DELETE FROM disciplina WHERE disc_codigo = {str(valor_id)}")
    banco.commit()   # EXCLUIR NO BANCO DE DADOS
  
def excluir_aluno(): # EXCLUIR ALUNO
    excluir = lista_alunos.tableWidget.currentRow()
    lista_alunos.tableWidget.removeRow(excluir)
    
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM aluno")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[excluir][0]
    cursor.execute(f"DELETE FROM aluno WHERE id= {str(valor_id)}")
    banco.commit()   # EXCLUIR NO BANCO DE DADOS  
  
  
            
def abrir_lista_prof():  # LISTA DE TODOS OS PROFESSORES CADASTRADOS
    lista_prof.show()
     
    # MOSTRAR LISTA DE PROFESSORES
    cursor = banco.cursor()  
    comando_SQL = "SELECT * FROM professor"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()       
    
    lista_prof.tableWidget.setRowCount(len(dados_lidos))
    lista_prof.tableWidget.setColumnCount(4)
    
    for i in range(0, len(dados_lidos)):  # FOR PARA MOSTAR OS DADOS LIDOS
        for j in range(0, 4):
            lista_prof.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def abrir_lista_disc():  # LISTA DE TODOS AS DISCIPLINAS CADASTRADAS
    lista_disc.show()
     
    # MOSTRAR LISTA DE PROFESSORES
    cursor = banco.cursor()  
    comando_SQL = "SELECT * FROM disciplina"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()       
    
    lista_disc.tableWidget.setRowCount(len(dados_lidos))
    lista_disc.tableWidget.setColumnCount(4)
    
    for i in range(0, len(dados_lidos)):  # FOR PARA MOSTAR OS DADOS LIDOS
        for j in range(0, 4):
            lista_disc.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                                     
def abrir_lista_alunos():  # LISTA DE TODOS OS ALUNOS CADASTRADOS
    lista_alunos.show()
     
    # MOSTRAR LISTA DE ALUNOS
    cursor = banco.cursor()  
    comando_SQL = "SELECT * FROM aluno"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()       
    
    lista_alunos.tableWidget.setRowCount(len(dados_lidos))
    lista_alunos.tableWidget.setColumnCount(5)
    
    for i in range(0, len(dados_lidos)):  # FOR PARA MOSTAR OS DADOS LIDOS
        for j in range(0, 5):
            lista_alunos.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            

def gerar_pdf_alunos(): # GERADOR DO PDF ALUNOS
   cursor = banco.cursor()
   comando_SQL = "SELECT * FROM aluno"
   cursor.execute(comando_SQL)
   dados_lidos = cursor.fetchall()
   y = 0
   pdf = canvas.Canvas("cadastro_todos_alunos.pdf")
   pdf.setFont("Times-Bold", 18)
   pdf.drawString(200,800, "Lista de Todos os Alunos Cadastrados:")
   pdf.setFont("Times-Bold", 13)
   
   pdf.drawString(10,750, "ID")
   pdf.drawString(50,750, "Código")
   pdf.drawString(110,750, "Nome")
   pdf.drawString(200,750, "Endereço")
   pdf.drawString(450,750, "Cidade")
   
   for i in range(0, len(dados_lidos)):
       y = y + 50
       pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
       pdf.drawString(50,750 - y, str(dados_lidos[i][1]))
       pdf.drawString(110,750 - y, str(dados_lidos[i][2]))
       pdf.drawString(200,750 - y, str(dados_lidos[i][3]))
       pdf.drawString(450,750 - y, str(dados_lidos[i][4]))

   pdf.save()
   print("PDF foi gerado com sucesso!")
    
def gerar_pdf_professores(): # GERADOR DO PDF ALUNOS
   cursor = banco.cursor()
   comando_SQL = "SELECT * FROM professor"
   cursor.execute(comando_SQL)
   dados_lidos = cursor.fetchall()
   y = 0
   pdf = canvas.Canvas("cadastro_todos_professores.pdf")
   pdf.setFont("Times-Bold", 18)
   pdf.drawString(200,800, "Lista de Todos os Professores Cadastrados:")
   pdf.setFont("Times-Bold", 13)
   
   pdf.drawString(10,750, "Código")
   pdf.drawString(80,750, "Nome")
   pdf.drawString(180,750, "Endereço")
   pdf.drawString(450,750, "Cidade")
   
   for i in range(0, len(dados_lidos)):
       y = y + 50
       pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
       pdf.drawString(80,750 - y, str(dados_lidos[i][1]))
       pdf.drawString(180,750 - y, str(dados_lidos[i][2]))
       pdf.drawString(450,750 - y, str(dados_lidos[i][3]))
    
   pdf.save()
   print("PDF FOI GERADO COM SUCESSO!")
   
def gerar_pdf_disciplina(): # GERADOR DO PDF DISCIPLINA
   cursor = banco.cursor()
   comando_SQL = "SELECT * FROM disciplina"
   cursor.execute(comando_SQL)
   dados_lidos = cursor.fetchall()
   y = 0
   pdf = canvas.Canvas("cadastro_todos_disciplina.pdf")
   pdf.setFont("Times-Bold", 18)
   pdf.drawString(200,800, "Lista de Todos as Disciplinas Cadastrados:")
   pdf.setFont("Times-Bold", 13)
   
   pdf.drawString(10,750, "Código")
   pdf.drawString(100,750, "Disciplina")
   pdf.drawString(250,750, "Curso")
   pdf.drawString(450,750, "Número de Aulas")
   
   for i in range(0, len(dados_lidos)):
       y = y + 50
       pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
       pdf.drawString(100,750 - y, str(dados_lidos[i][1]))
       pdf.drawString(250,750 - y, str(dados_lidos[i][2]))
       pdf.drawString(450,750 - y, str(dados_lidos[i][3]))
    
   pdf.save()
   print("PDF FOI GERADO COM SUCESSO!")   
   
   
app = QtWidgets.QApplication([])

menu = uic.loadUi("menu_inicial.ui") # MENU INICIAL
menu_opcao = uic.loadUi("menu_opcao2.ui") # MENU MAIS OPÇOES
lista_alunos = uic.loadUi("lista_alunos.ui") # LISTA DE TODOS ALUNOS
lista_prof = uic.loadUi("lista_prof.ui") # LISTA DE TODOS OS PROFESSORES
lista_disc = uic.loadUi("lista_disc.ui") # LISTA DE TODAS AS DISCIPLINAS

cad_aluno = uic.loadUi("cadastro_aluno.ui")  # CADASTRO DE ALUNO
cad_prof = uic.loadUi("cadastro_prof.ui") # CADASTRO DE PROFESSORES
cad_disc = uic.loadUi("cadastro_disc.ui") # CADASTRO DE DISCIPLINAS
cad_mat = uic.loadUi("cadastro_mat.ui") # CADASTRAR MATRICULA

edit_aluno = uic.loadUi("editar_aluno.ui") # EDIÇÃO DE ALUNO
edit_prof = uic.loadUi("editar_prof.ui") # EDIÇÃO DE PROFESSOR
edit_disc = uic.loadUi("editar_disc.ui") # EDIÇÃO DAS DISCIPLINAS

menu.mais_op.clicked.connect(abrir_menuop) # ABRIR MENU LISTA DE MAIS OPÇÕES

cad_aluno.cad_aluno2.clicked.connect(cadastro_aluno)  # SALVAR CADASTRO ALUNO
cad_prof.cad_prof2.clicked.connect(cadastro_prof) # SALVAR CADASTRO PROFESSOR
cad_disc.cad_disc2.clicked.connect(cadastro_disc) # SALVAR CADASTRO DISCIPLINA

menu.cad_disc.clicked.connect(abrir_menu_disc) # ABRIR MENU DISCIPLINA
menu.cad_aluno.clicked.connect(abrir_menu_aluno) # ABRIR MENU DO ALUNO
menu.cad_prof.clicked.connect(abrir_menu_prof) # ABRIR MENU DO PROFESSOR
menu.cad_matricula.clicked.connect(abrir_menu_mat) # ABRIR MENU MATRICULA


menu_opcao.list_aluno.clicked.connect(abrir_lista_alunos) # ABRIR MENU LISTA DE ALUNOS
menu_opcao.list_prof2.clicked.connect(abrir_lista_prof) # ABRIR MENU LISTA DE PROFESSORES
menu_opcao.list_disc.clicked.connect(abrir_lista_disc) # ABRIR MENU LISTA DE DISCIPLINAS

lista_alunos.editar_aluno.clicked.connect(editar_aluno) # EDITAR ALUNO
lista_prof.editar_prof.clicked.connect(editar_prof) # EDITAR PROFESSOR
lista_disc.editar_disc.clicked.connect(editar_disc) # EDITAR DISCIPLINA

lista_alunos.excluir_aluno.clicked.connect(excluir_aluno) # EXCLUIR ALUNOS
lista_prof.excluir_prof.clicked.connect(excluir_prof) # EXCLUIR PROFESSOR
lista_disc.excluir_disc.clicked.connect(excluir_disc) # EXCLUIR DISCIPLINA

lista_alunos.pdf_aluno.clicked.connect(gerar_pdf_alunos) # GERAR PDF DE TODOS OS ALUNOS CADASTRADOS
lista_prof.pdf_prof.clicked.connect(gerar_pdf_professores) #GERAR PDF DE TODOS OS PROFESSORES CADASTRADOS
lista_disc.pdf_disc.clicked.connect(gerar_pdf_disciplina) # GERAR PDF DE TODAS AS DISCIPLINAS CADASTRADAS

edit_aluno.salvar_edit_aluno.clicked.connect(salvar_edit_aluno) # SALVAR EDIÇÃO DE ALUNO
edit_prof.salvar_edit_prof.clicked.connect(salvar_edit_prof) # SALVAR EDIÇÃO DO PROFESSOR
edit_disc.salvar_edit_disc.clicked.connect(salvar_edit_disc) # SALVAR EDIÇÃO DE DISCIPLINA



menu.show()
app.exec()
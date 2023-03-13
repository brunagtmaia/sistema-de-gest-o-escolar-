from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

banco = mysql.connector.connect(
    host='localhost', database='cadastro_teste', 
    user='root', password='')

if banco.is_connected():
    db_info = banco.get_server_info()
    print("Conectado ao servidor MySQL versão:", db_info)
    cursor = banco.cursor()
    cursor.execute('select database();')
    linha = cursor.fetchone()
    print("Conectado ao banco de dados ", linha)
    
""""
if banco.is_connected():
    cursor.close()
    banco.close()
    print("Conexão ao MySQL foi encerrada")
"""

def salvar_dados_editados():
    #pega o numeor do id
    global numero_id
    
    # valor diigitado no campo de edicoes
    codigo = tela_editar.codigo_edit.text()
    descricao = tela_editar.produto_edit.text()
    preco = tela_editar.preco_edit.text()
    categoria = tela_editar.categoria_edit.text()
    
    # atualizar os dados no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}" .format(codigo, descricao, preco, categoria, numero_id))
    banco.commit()
    
    #atualizar as janelas
    tela_editar.close()
    lista_produtos.close()
    listagem_produtos()
    
    
def editar_dados():
    global numero_id
    editar = lista_produtos.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[editar][0]
    cursor.execute(f"SELECT * FROM produtos WHERE id={str(valor_id)}")
    produto = cursor.fetchall()
    tela_editar.show()
    
    numero_id = valor_id
    
    tela_editar.id_edit.setText(str(produto[0][0]))
    tela_editar.codigo_edit.setText(str(produto[0][1]))
    tela_editar.produto_edit.setText(str(produto[0][2]))
    tela_editar.preco_edit.setText(str(produto[0][3]))
    tela_editar.categoria_edit.setText(str(produto[0][4]))
    
    
def excluir_dados(): # EXCLUIR DADOS
    excluir = lista_produtos.tableWidget.currentRow()
    lista_produtos.tableWidget.removeRow(excluir)
    
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[excluir][0]
    cursor.execute(f"DELETE FROM produtos WHERE id= {str(valor_id)}")
    banco.commit()   # EXCLUIR NO BANCO DE DADOS
    
def gerar_pdf(): # GERADOR DO PDF
   cursor = banco.cursor()
   comando_SQL = "SELECT * FROM produtos"
   cursor.execute(comando_SQL)
   dados_lidos = cursor.fetchall()
   y = 0
   pdf = canvas.Canvas("cadastro_produtos.pdf")
   pdf.setFont("Times-Bold", 18)
   pdf.drawString(200,800, "Produtos cadastrados:")
   pdf.setFont("Times-Bold", 13)
   
   pdf.drawString(10,750, "ID")
   pdf.drawString(110,750, "Código")
   pdf.drawString(210,750, "Produto")
   pdf.drawString(310,750, "Preço")
   pdf.drawString(410,750, "Categoria")
   
   for i in range(0, len(dados_lidos)):
       y = y + 50
       pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
       pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
       pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
       pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
       pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

   pdf.save()
   print("PDF foi gerado com sucesso!")
       
   
def listagem_produtos():  # SEGUNDA TELA (LISTA DE PRODUTOS CADASTRADOS)
    lista_produtos.show()
     
    # MOSTRAR LISTA DE PRODUTOS 
    cursor = banco.cursor()  
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()       
    
    lista_produtos.tableWidget.setRowCount(len(dados_lidos))
    lista_produtos.tableWidget.setColumnCount(5)
    
    for i in range(0, len(dados_lidos)):  # FOR PARA MOSTAR OS DADOS LIDOS
        for j in range(0, 5):
            lista_produtos.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
    
    
       
def funcao_principal():
    linha1 = cadastro.codigo_box.text()
    linha2 = cadastro.descricao_box.text()
    linha3 = cadastro.preco_box.text()
    categoria = ''
    
    if cadastro.informatica.isChecked():
        print("Categoria: Informática")
        categoria = "Informática"
    
    elif cadastro.alimentos.isChecked():
        print("Categoria: Alimentos")
        categoria = "Alimento"
        
    elif cadastro.eletronico.isChecked():
        print("Categoria: Eletrônico")
        categoria = "Eletrônico"
    
    else:
        print("Nenhuma Categoria Selecionada")
        categoria = "Não Selecionada"
        
    print("Código:", linha1)
    print("Descrição:", linha2)
    print("Preço:", linha3)
    
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    cadastro.codigo_box.setText("")  # LIMPAR CAMPO CODIGO
    cadastro.descricao_box.setText("") # LIMPAR CAMPO DESCRICAO
    cadastro.preco_box.setText("") # LIMPAR CAMPO PREÇO
    
app = QtWidgets.QApplication([])
cadastro = uic.loadUi("cadastro01.ui")
lista_produtos = uic.loadUi("lista_produtos.ui")
tela_editar = uic.loadUi("editar.ui")
cadastro.pushButton.clicked.connect(funcao_principal) # BOTAO SALVAR DADOS NA TABELA
cadastro.pushButton_2.clicked.connect(listagem_produtos) # ABRIR TELA LISTA DE PRODUTOS
lista_produtos.pdf_button.clicked.connect(gerar_pdf) # BOTAO GERADOR DE PDF
lista_produtos.excluir_button.clicked.connect(excluir_dados) # BOTAO EXCLUIR DADOS DA TABELA
lista_produtos.editar_button.clicked.connect(editar_dados)    # BOTAO EDITAR  DADOS DA TABELA
tela_editar.salvar_edit.clicked.connect(salvar_dados_editados) # SALVAR OS DADOS QUE FORAM EDITADOS NA TELA EDICAO

cadastro.show()
app.exec()


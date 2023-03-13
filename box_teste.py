from PyQt5 import uic, QtWidgets


#def opcao_selec():
    
    #cidade = tela.box.currentText()
    #tela.label_2.setText(f"Cidade: {cidade}")
    #print(cidade)

app = QtWidgets.QApplication([])
tela = uic.loadUi("box_teste.ui")

tela.box.addItems(["São Paulo","Rio de Janeiro","Minas Gerais","Ceará","Espirito Santo"])
#tela.pushButton.clicked.connect(opcao_selec)

tela.show()
app.exec()
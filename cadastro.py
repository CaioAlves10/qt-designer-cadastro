from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import mysql.connector

banco = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '',
    database = 'cadastro',
)
def cadastro():
    exibir = tela1.nome.text() and tela1.email.text() and tela1.telefone.text()

    if exibir == '':
        QMessageBox.about(tela1, 'Atenção', 'Preencha os campos solicitados')
    else:
        nome = tela1.nome.text()
        email = tela1.email.text()
        telefone = tela1.telefone.text()

        sexo = ''
        if tela1.feminino.isChecked():
            sexo = 'feminino'
        elif tela1.masculino.isChecked():
            sexo = 'masculino'
        else:
            sexo = 'não definido'
        cursor = banco.cursor() #interagir com o banco de dados
        sql = "INSERT INTO cadastrar (nome, email, telefone, sexo)" \
            "VALUES (%s, %s, %s, %s)"
        colunas = (str(nome), str(email), str(telefone), sexo) #converter string(%s) para colunas do banco
        cursor.execute(sql, colunas)
        banco.commit()

        QMessageBox.about(tela1, 'Salvo com sucesso', 'Informações registradas com sucesso')
        tela1.nome.setText("")
        tela1.email.setText("")
        tela1.telefone.setText("")
        tela1.sexo.setText("")

def exibir():
    tela2.show()
    tela1.close()
    cursor = banco.cursor()
    sql = "SELECT * FROM cadastrar"
    cursor.execute(sql)
    dados = cursor.fetchall() #retorna linhas e colunas da tabela
    tela2.tabelaCadastro.setRowCount(len(dados)) #numero de linhas
    tela2.tabelaCadastro.setColumnCount(6) #numero de colunas

    for contador in range(0, len(dados)): #mostra as colunas
        for acessar in range(0,6): #mostra os dados em linha
            tela2.tabelaCadastro.setItem(contador, acessar, QtWidgets.QTableWidgetItem(str(dados[contador][acessar])))


app = QtWidgets.QApplication([])
tela1 = uic.loadUi("cadastro.ui")
tela2 = uic.loadUi("tabelaCadastro.ui")
tela1.botaoCadastrar.clicked.connect(cadastro)
tela1.botaoExibir.clicked.connect(exibir)
tela1.show()
app.exec()
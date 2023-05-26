from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from reportlab.pdfgen import canvas

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

def salvarPDF():
    cursor = banco.cursor()
    sql = "SELECT * FROM cadastrar"
    cursor.execute(sql)
    dados = cursor.fetchall()
    x = 0
    pdf = canvas.Canvas("alunos.pdf")
    pdf.setFont("Courier-Bold", 22)
    pdf.drawString(100, 800, "Alunos cadastrados") #Coordenadas e título
    pdf.line(50, 740, 540, 740) #Coordenadas da tabela
    pdf.setFont("Courier", 10)
    pdf.drawString(110, 750, "Nome")
    pdf.drawString(210, 750, "E-mail")
    pdf.drawString(400, 750, "Telefone")
    pdf.drawString(510, 750, "Sexo")

    for i in range(0, len(dados)):
        x = x + 20
        pdf.drawString(10, 750 - x, str(dados[i][0]))
        pdf.drawString(110, 750 - x, str(dados[i][1]))
        pdf.drawString(210, 750 - x, str(dados[i][2]))
        pdf.drawString(400, 750 - x, str(dados[i][3]))
        pdf.drawString(50, 750 - x, str(dados[i][4]))
    pdf.save()
    QMessageBox.about(tela2, "PDF GERADO", "PDF BAIXADO COM SUCESSO")

app = QtWidgets.QApplication([])
tela1 = uic.loadUi("cadastro.ui")
tela2 = uic.loadUi("tabelaCadastro.ui")
tela1.botaoCadastrar.clicked.connect(cadastro)
tela1.botaoExibir.clicked.connect(exibir)
tela2.botaoSalvarPDF.clicked.connect(salvarPDF)
tela1.show()
app.exec()
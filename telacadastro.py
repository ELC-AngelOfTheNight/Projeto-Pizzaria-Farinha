import mysql.connector
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QWidget

class TelaCadastro(QWidget):
    def __init__(self, gerenciador):
        super().__init__()
        self.gerenciador = gerenciador
        # Carrega a interface no próprio objeto QWidget
        uic.loadUi("./cadastro.ui", self)
        
        # Conecta os botões
        self.btn_criar.clicked.connect(self.salvar)
        self.btn_screenmanager.clicked.connect(self.ir_para_login)

    def connect(self):
        return mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="ds"
        )

    def salvar(self):
        try:
            usuario = str(self.txt_usuario.text())
            email = str(self.txt_email.text())
            senha = str(self.txt_senha.text())

            conn = self.connect()
            cursor = conn.cursor()
            SQL = "SELECT * FROM tb_usuarios WHERE usuario = %s OR email = %s"
            cursor.execute(SQL, (usuario, email)) 

            if len(cursor.fetchall()) > 0:
                mensagem = QMessageBox()
                mensagem.setIcon(QMessageBox.Icon.Information)
                mensagem.setText('Cadastro já existente!')
                mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
                mensagem.exec()
            else:
                SQL = "INSERT INTO tb_usuarios (usuario, email, senha) VALUES (%s, %s, %s)"
                cursor.execute(SQL, (usuario, email, senha)) 
                conn.commit()
                
                mensagem = QMessageBox()
                mensagem.setText("Dados enviados com sucesso!")
                mensagem.setWindowTitle("CADASTRO DE CONTAS")
                mensagem.setIcon(QMessageBox.Icon.Information)
                mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
                mensagem.exec()

                self.txt_usuario.setText("")
                self.txt_email.setText("")
                self.txt_senha.setText("")
                self.txt_usuario.setFocus()
                
            cursor.close()
            conn.close()
        except Exception as e:
            mensagem = QMessageBox()
            mensagem.setIcon(QMessageBox.Icon.Critical)
            mensagem.setText(f'Erro ao salvar os dados: {e}')
            mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
            mensagem.exec()

    def ir_para_login(self):
        self.gerenciador.abrir_login()
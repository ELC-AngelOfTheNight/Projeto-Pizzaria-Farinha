import mysql.connector
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QWidget

class TelaLogin(QWidget):
    def __init__(self, gerenciador):
        super().__init__()
        self.gerenciador = gerenciador
        uic.loadUi("./login.ui", self)
        
        self.btn_screenmanager.clicked.connect(self.ir_para_cadastro)
        self.btn_logar.clicked.connect(self.verificar)

    def connect(self):
        return mysql.connector.connect(
            user="root", password="", host="localhost", database="ds"
        )

    def verificar(self):
        conn = None
        try:
            usuario_email = self.txt_usuario_email.text()
            senha = self.txt_senha.text()

            conn = self.connect()
            cursor = conn.cursor()

            SQL = "SELECT * FROM tb_usuarios WHERE (usuario = %s OR email = %s) AND senha = %s"
            cursor.execute(SQL, (usuario_email, usuario_email, senha))
            
            resultado = cursor.fetchone() # Guarda o resultado da busca

            if resultado:
                # Na tabela da imagem, as colunas são: id_cliente (0), usuario (1), email (2), senha (3)
                nome_usuario_logado = resultado[1] 

                mensagem = QMessageBox()
                mensagem.setIcon(QMessageBox.Icon.Information)
                mensagem.setText(f"Bem-vindo, {nome_usuario_logado}!")
                mensagem.setWindowTitle("BEM-VINDO")
                mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
                mensagem.exec()
                
                self.txt_usuario_email.clear()
                self.txt_senha.clear()
                
                # Passa o nome do usuário para o gerenciador de telas
                self.gerenciador.abrir_gerenciador(nome_usuario_logado)
            else:
                mensagem = QMessageBox()
                mensagem.setText("Dados não condizentes!")
                mensagem.setWindowTitle("ERRO")
                mensagem.setIcon(QMessageBox.Icon.Critical)
                mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
                mensagem.exec()

                self.txt_usuario_email.setText("")
                self.txt_senha.setText("")
                self.txt_usuario_email.setFocus()

            cursor.close()
        except Exception as e:
            mensagem = QMessageBox()
            mensagem.setIcon(QMessageBox.Icon.Critical)
            mensagem.setText(f"Erro ao logar na conta: {e}")
            mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
            mensagem.exec()
        finally:
            if conn and conn.is_connected():
                conn.close()

    def ir_para_cadastro(self):
        self.gerenciador.abrir_cadastro()
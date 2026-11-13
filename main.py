import sys
from PyQt6 import QtWidgets
from telacadastro import TelaCadastro
from telalogin import TelaLogin
from gerenciador import TelaGerenciador 

class GerenciadorDeTelas:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        
        self.tela_cadastro = TelaCadastro(self)
        self.tela_login = TelaLogin(self)
        self.tela_gerenciador = TelaGerenciador(self)

    def iniciar(self):
        self.tela_login.show() 
        sys.exit(self.app.exec())

    def abrir_login(self):
        self.tela_cadastro.hide()
        self.tela_gerenciador.hide()
        self.tela_login.show()

    def abrir_cadastro(self):
        self.tela_login.hide()
        self.tela_gerenciador.hide()
        self.tela_cadastro.show()

    # Recebe quem logou como parâmetro
    def abrir_gerenciador(self, usuario_logado):
        self.tela_login.hide()
        self.tela_cadastro.hide()
        self.tela_gerenciador.definir_usuario(usuario_logado) # Função nova que criaremos abaixo
        self.tela_gerenciador.carregar_dados() 
        self.tela_gerenciador.show()

if __name__ == "__main__":
    gerenciador = GerenciadorDeTelas()
    gerenciador.iniciar()
import mysql.connector
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem

class TelaGerenciador(QWidget):
    def __init__(self, gerenciador):
        super().__init__()
        self.gerenciador = gerenciador
        uic.loadUi("./gerenciador.ui", self)
        
        self.btn_adicionar.clicked.connect(self.adicionar)
        self.btn_atualizar.clicked.connect(self.atualizar)
        self.btn_deletar.clicked.connect(self.deletar)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_sair.clicked.connect(self.fazer_logout)
        
        self.tabela_usuarios.itemClicked.connect(self.preencher_campos_ao_clicar)

    def connect(self):
        return mysql.connector.connect(
            user="root", password="", host="localhost", database="ds"
        )
        
    # -------- NOVO METODO: Altera a Label do canto da tela -----------
    def definir_usuario(self, nome_usuario):
        self.lbl_usuario_logado.setText(f"👤 Logado como: {nome_usuario}")
    # -----------------------------------------------------------------

    def carregar_dados(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, usuario, email, senha FROM tb_usuarios")
            dados = cursor.fetchall()
            
            self.tabela_usuarios.setRowCount(len(dados))
            for linha_idx, linha_dados in enumerate(dados):
                for col_idx, valor in enumerate(linha_dados):
                    self.tabela_usuarios.setItem(linha_idx, col_idx, QTableWidgetItem(str(valor)))
            
            cursor.close()
            conn.close()
        except Exception as e:
            self.mostrar_mensagem("ERRO", f"Erro ao carregar dados: {e}", QMessageBox.Icon.Critical)

    def adicionar(self):
        usuario = self.txt_usuario.text()
        email = self.txt_email.text()
        senha = self.txt_senha.text()

        if not usuario or not email or not senha:
            self.mostrar_mensagem("Aviso", "Preencha todos os campos!", QMessageBox.Icon.Warning)
            return

        try:
            conn = self.connect()
            cursor = conn.cursor()
            SQL = "INSERT INTO tb_usuarios (usuario, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(SQL, (usuario, email, senha))
            conn.commit()
            
            self.limpar_campos()
            self.carregar_dados()
            self.mostrar_mensagem("Sucesso", "Usuário adicionado com sucesso!", QMessageBox.Icon.Information)
            
            cursor.close()
            conn.close()
        except Exception as e:
            self.mostrar_mensagem("ERRO", f"Erro ao adicionar: {e}", QMessageBox.Icon.Critical)

    def atualizar(self):
        id_cliente = self.txt_id.text()
        usuario = self.txt_usuario.text()
        email = self.txt_email.text()
        senha = self.txt_senha.text()

        if not id_cliente:
            self.mostrar_mensagem("Aviso", "Selecione um usuário na tabela para atualizar!", QMessageBox.Icon.Warning)
            return

        try:
            conn = self.connect()
            cursor = conn.cursor()
            SQL = "UPDATE tb_usuarios SET usuario=%s, email=%s, senha=%s WHERE id_cliente=%s"
            cursor.execute(SQL, (usuario, email, senha, id_cliente))
            conn.commit()
            
            self.limpar_campos()
            self.carregar_dados()
            self.mostrar_mensagem("Sucesso", "Usuário atualizado com sucesso!", QMessageBox.Icon.Information)
            
            cursor.close()
            conn.close()
        except Exception as e:
            self.mostrar_mensagem("ERRO", f"Erro ao atualizar: {e}", QMessageBox.Icon.Critical)

    def deletar(self):
        id_cliente = self.txt_id.text()

        if not id_cliente:
            self.mostrar_mensagem("Aviso", "Selecione um usuário na tabela para deletar!", QMessageBox.Icon.Warning)
            return

        resposta = QMessageBox.question(self, "Confirmar", f"Tem certeza que deseja deletar o ID {id_cliente}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if resposta == QMessageBox.StandardButton.Yes:
            try:
                conn = self.connect()
                cursor = conn.cursor()
                SQL = "DELETE FROM tb_usuarios WHERE id_cliente=%s"
                cursor.execute(SQL, (id_cliente,))
                conn.commit()
                
                self.limpar_campos()
                self.carregar_dados()
                self.mostrar_mensagem("Sucesso", "Usuário deletado!", QMessageBox.Icon.Information)
                
                cursor.close()
                conn.close()
            except Exception as e:
                self.mostrar_mensagem("ERRO", f"Erro ao deletar: {e}", QMessageBox.Icon.Critical)

    def preencher_campos_ao_clicar(self, item):
        linha = item.row()
        self.txt_id.setText(self.tabela_usuarios.item(linha, 0).text())
        self.txt_usuario.setText(self.tabela_usuarios.item(linha, 1).text())
        self.txt_email.setText(self.tabela_usuarios.item(linha, 2).text())
        self.txt_senha.setText(self.tabela_usuarios.item(linha, 3).text())

    def limpar_campos(self):
        self.txt_id.clear()
        self.txt_usuario.clear()
        self.txt_email.clear()
        self.txt_senha.clear()

    def fazer_logout(self):
        self.limpar_campos()
        self.tabela_usuarios.setRowCount(0)
        self.gerenciador.abrir_login()

    def mostrar_mensagem(self, titulo, texto, icone):
        msg = QMessageBox()
        msg.setWindowTitle(titulo)
        msg.setText(texto)
        msg.setIcon(icone)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

import sqlite3
import os
import customtkinter as ctk
from tkinter import messagebox

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Descobre exatamente onde este arquivo .py está salvo no computador
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(diretorio_atual, "sistema.db")

# Conecta ao banco usando o caminho completo e seguro
conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

# Cria a tabela caso ela ainda não exista
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        nome TEXT,
        preco REAL,
        quantidade INTEGER
    )
""")
conexao.commit()

# --- FUNÇÕES DO BANCO DE DADOS E LÓGICA DO SISTEMA ---

def cadastrar_produto_bd(nome, preco, quantidade):
    try:
        cursor.execute(
            "INSERT INTO produtos VALUES (?, ?, ?)",
            (nome, preco, quantidade)
        )
        conexao.commit()
        return True, "Sucesso! Produto cadastrado."
    except sqlite3.Error as erro:
        return False, f"Erro ao cadastrar o produto: {erro}"

def consultar_produtos_bd():
    cursor.execute("SELECT * FROM produtos")
    return cursor.fetchall()


# --- INTERFACE GRÁFICA: SISTEMA PRINCIPAL ---

def abrir_sistema_principal():
    # Encerra e destrói a janela de login atual da memória
    janela_login.destroy()

    # Cria a janela principal do sistema
    janela = ctk.CTk()
    janela.title("Lanchonete Ennius Muniz - Senac-DF")
    janela.geometry("500x450")

    titulo = ctk.CTkLabel(janela, text="Controle de Produtos (SQLite)", font=ctk.CTkFont(size=20, weight="bold"))
    titulo.pack(pady=20)

    # Frame para Cadastro
    frame_cadastro = ctk.CTkFrame(janela)
    frame_cadastro.pack(pady=10, padx=20, fill="x")

    lbl_cad = ctk.CTkLabel(frame_cadastro, text="Cadastrar Novo Produto", font=ctk.CTkFont(size=14, weight="bold"))
    lbl_cad.pack(pady=5)

    entry_nome = ctk.CTkEntry(frame_cadastro, placeholder_text="Nome do produto")
    entry_nome.pack(pady=5, padx=10, fill="x")

    entry_preco = ctk.CTkEntry(frame_cadastro, placeholder_text="Preço (Ex: 5.00)")
    entry_preco.pack(pady=5, padx=10, fill="x")

    entry_qtd = ctk.CTkEntry(frame_cadastro, placeholder_text="Quantidade em estoque (Ex: 10)")
    entry_qtd.pack(pady=5, padx=10, fill="x")

    def acao_cadastrar():
        nome = entry_nome.get().strip()
        try:
            preco = float(entry_preco.get().replace(",", "."))
            quantidade = int(entry_qtd.get())
            
            if not nome:
                messagebox.showerror("Erro", "O nome do produto não pode estar vazio.")
                return

            sucesso, msg = cadastrar_produto_bd(nome, preco, quantidade)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                entry_nome.delete(0, 'end')
                entry_preco.delete(0, 'end')
                entry_qtd.delete(0, 'end')
            else:
                messagebox.showerror("Erro", msg)
        except ValueError:
            messagebox.showerror("Erro", "Digite valores válidos para preço e quantidade.")

    btn_cadastrar = ctk.CTkButton(frame_cadastro, text="Salvar Produto", command=acao_cadastrar)
    btn_cadastrar.pack(pady=10)

    # Frame para Consulta
    frame_consulta = ctk.CTkFrame(janela)
    frame_consulta.pack(pady=10, padx=20, fill="both", expand=True)

    lbl_cons = ctk.CTkLabel(frame_consulta, text="Produtos Cadastrados", font=ctk.CTkFont(size=14, weight="bold"))
    lbl_cons.pack(pady=5)

    # Caixa de texto rolável para exibir os produtos
    texto_produtos = ctk.CTkTextbox(frame_consulta, height=120)
    texto_produtos.pack(pady=5, padx=10, fill="both", expand=True)

    def acao_consultar():
        texto_produtos.delete("0.0", "end")
        itens = consultar_produtos_bd()
        if not itens:
            texto_produtos.insert("0.0", "Nenhum produto cadastrado no banco de dados.")
            return
        
        resultado = "-" * 45 + "\n"
        for linha in itens:
            resultado += f"Produto: {linha[0]:<12} | R$ {linha[1]:>6.2f} | Est: {linha[2]}\n"
        resultado += "-" * 45
        texto_produtos.insert("0.0", resultado)

    btn_consultar = ctk.CTkButton(frame_consulta, text="Atualizar Lista", command=acao_consultar)
    btn_consultar.pack(pady=5)

    # Carrega os produtos inicialmente
    acao_consultar()

    janela.mainloop()


# --- INTERFACE GRÁFICA: BARREIRA DE AUTENTICAÇÃO (LOGIN) ---

def validar_login():
    usuario = entry_user.get()
    senha = entry_senha.get()

    # Credenciais simples de exemplo (pode ajustar conforme necessário)
    if usuario == "admin" and senha == "1234":
        abrir_sistema_principal()
    else:
        messagebox.showerror("Erro de Autenticação", "Usuário ou senha incorretos!")

# BLOCO A: A Interface da Barreira[cite: 1]
janela_login = ctk.CTk()
janela_login.title("Login - Lanchonete Ennius Muniz")
janela_login.geometry("300x350")

lbl_titulo_login = ctk.CTkLabel(janela_login, text="Acesso ao Sistema", font=ctk.CTkFont(size=16, weight="bold"))
lbl_titulo_login.pack(pady=20)

entry_user = ctk.CTkEntry(janela_login, placeholder_text="Usuário")
entry_user.pack(pady=10)

# NOVO: Oculta o texto digitado na tela
entry_senha = ctk.CTkEntry(janela_login, placeholder_text="Senha", show="*")
entry_senha.pack(pady=10)

ctk.CTkButton(janela_login, text="Autenticar", command=validar_login).pack(pady=30)

janela_login.mainloop()

# Fecha a conexão com o banco ao encerrar completamente o fluxo
conexao.close()
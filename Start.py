import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os

# Definindo cores
VERDE = "#6B8E23"
BRANCO = "#FFFFFF"

def salvar_score(iniciais, score):
    with open("scores.txt", "a") as arquivo:
        arquivo.write(f"{iniciais}: {score}\n")

def mostrar_scores():
    scores = mostrar_scores_file()

    # Limpa a tela inicial
    for widget in initial_window.winfo_children():
        widget.destroy()

    # Título da janela principal
    title_label = tk.Label(initial_window, text="Scores", font=("Arial", 20), bg=VERDE, fg=BRANCO)
    title_label.pack(pady=10)

    # Exibição dos scores
    if scores:
        for score in scores:
            score_label = tk.Label(initial_window, text=score.strip(), font=("Arial", 12), bg=VERDE, fg=BRANCO)
            score_label.pack()
    else:
        empty_label = tk.Label(initial_window, text="Ainda não há scores salvos.", font=("Arial", 12), bg=VERDE, fg=BRANCO)
        empty_label.pack()

    # Botão para voltar à tela inicial
    back_button = tk.Button(initial_window, text="Voltar", font=("Arial", 12), command=mostrar_tela_inicial)
    back_button.pack(pady=10)

def mostrar_scores_file():
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as arquivo:
            scores = arquivo.readlines()
            return scores
    else:
        return []
pontuacao_jogador = 0

def iniciar_jogo():
    global pontuacao_jogador
    pontuacao_jogador = 0
    messagebox.showinfo("Iniciar Jogo", "Jogo iniciado!")
    # Aqui você pode adicionar a lógica do seu jogo, onde a pontuação do jogador é atualizada
    # Exemplo: pontuacao_jogador += 10

def finalizar_jogo():
    global pontuacao_jogador
    # Aqui você pode adicionar a lógica para finalizar o jogo e salvar a pontuação do jogador
    salvar_score("JOG", pontuacao_jogador)
    messagebox.showinfo("Fim do Jogo", f"Você marcou {pontuacao_jogador} pontos!")

def mostrar_tela_inicial():
    # Restante do código aqui...

    # Botão para iniciar o jogo
    start_button = tk.Button(initial_window, text="Iniciar Jogo", font=("Arial", 12), command=iniciar_jogo)
    start_button.pack(pady=10)

    # Botão para finalizar o jogo
    end_button = tk.Button(initial_window, text="Finalizar Jogo", font=("Arial", 12), command=finalizar_jogo)
    end_button.pack(pady=10)

def adicionar_novo_jogador(score_window):
    novo_jogador = simpledialog.askstring("Novo Jogador", "Digite as iniciais do novo jogador:")
    if novo_jogador:
        salvar_score(novo_jogador, 0)
        messagebox.showinfo("Novo Jogador", "Novo jogador adicionado com sucesso!")
        score_window.destroy()
        mostrar_scores()
    else:
        messagebox.showerror("Erro", "Por favor, insira as iniciais do novo jogador.")

def excluir_pontuacao():
    jogador = simpledialog.askstring("Excluir Pontuação", "Digite as iniciais do jogador para excluir sua pontuação:")
    if jogador:
        scores = mostrar_scores_file()
        with open("scores.txt", "w") as arquivo:
            for score in scores:
                if jogador not in score:
                    arquivo.write(score)
        messagebox.showinfo("Pontuação Excluída", f"A pontuação do jogador {jogador} foi excluída com sucesso!")
    else:
        messagebox.showerror("Erro", "Por favor, insira as iniciais do jogador para excluir sua pontuação.")

def iniciar_jogo():
    messagebox.showinfo("Iniciar Jogo", "Jogo iniciado!")

def mostrar_tela_inicial():
    # Limpa a tela inicial
    for widget in initial_window.winfo_children():
        widget.destroy()

    # Título da janela principal
    title_label = tk.Label(initial_window, text="Bem-vindo ao jogo na Floresta!", font=("Arial", 20), bg=VERDE, fg=BRANCO)
    title_label.pack(pady=20)

    # Botão para ver scores
    scores_button = tk.Button(initial_window, text="Ver Scores", font=("Arial", 12), command=mostrar_scores)
    scores_button.pack(pady=10)

    # Botão para iniciar o jogo
    start_button = tk.Button(initial_window, text="Iniciar Jogo", font=("Arial", 12), command=iniciar_jogo)
    start_button.pack(pady=10)

    # Criando o menu de opções
    menu_bar = tk.Menu(initial_window)
    initial_window.config(menu=menu_bar)
    menu_opcoes = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Opções", menu=menu_opcoes)
    menu_opcoes.add_command(label="Adicionar Novo Jogador", command=lambda: adicionar_novo_jogador(initial_window))
    menu_opcoes.add_command(label="Excluir Pontuação", command=excluir_pontuacao)

if __name__ == "__main__":
    # Criando janela principal
    initial_window = tk.Tk()
    initial_window.title("Bem-vindo ao jogo na Floresta")

    # Estilizando a janela principal
    initial_window.configure(bg=VERDE)
    initial_window.geometry("600x400")

    mostrar_tela_inicial()

    initial_window.mainloop()

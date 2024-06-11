import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import importlib.util
import tkinter.font as tkFont
import pygame
import sys
from math import atan2, cos, sin
from pygame.math import Vector2
from random import randint

# Defining colors
VERDE = "#6B8E23"
BRANCO = "#FFFFFF"

# Function to load custom font
def load_custom_font():
    font_path = "PixeloidMono.ttf"
    custom_font = tkFont.Font(family="PixeloidMono", size=12)
    return custom_font

# Function to save score with player's points
def salvar_score(iniciais, pontos):
    with open("scores.txt", "a") as arquivo:
        arquivo.write(f"{iniciais}: {pontos}\n")

# Function to display scores
def mostrar_scores(initial_window):
    scores = mostrar_scores_file()

    # Clear the initial window
    for widget in initial_window.winfo_children():
        widget.destroy()

    # Title of the main window
    title_label = tk.Label(initial_window, text="Scores", font=custom_font_big, bg=VERDE, fg=BRANCO)
    title_label.pack(pady=10)

    # Display scores with buttons to start the game for each player
    if scores:
        for score in scores:
            player_initials, player_points = score.strip().split(":")
            score_button = tk.Button(initial_window, text=f"{player_initials} - {player_points}", font=custom_font_small, 
                                     command=lambda initials=player_initials: start_game_with_player(initials))
            score_button.pack(pady=5)
    else:
        empty_label = tk.Label(initial_window, text="No scores saved yet.", font=custom_font_small, bg=VERDE, fg=BRANCO)
        empty_label.pack()

    # Button to go back to the initial screen
    back_button = tk.Button(initial_window, text="Back", font=custom_font_small, command=mostrar_tela_inicial)
    back_button.pack(pady=10)

# Function to read scores from file
def mostrar_scores_file():
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as arquivo:
            scores = arquivo.readlines()
            return scores
    else:
        return []

# Function to start game with selected player's initials
def start_game_with_player(player_initials):
    initial_window.destroy()  # Close the scores window
    iniciar_jogo(player_initials)  # Start the game with the selected player's initials

# Function to add a new player
def adicionar_novo_jogador(score_window):
    novo_jogador = simpledialog.askstring("Novo Jogador", "Digite as iniciais do novo jogador:")
    if novo_jogador:
        salvar_score(novo_jogador, player.points)  # Save player's points along with initials
        messagebox.showinfo("Novo Jogador", "Novo jogador adicionado com sucesso!")
        score_window.destroy()
        mostrar_scores()
    else:
        messagebox.showerror("Erro", "Por favor, insira as iniciais do novo jogador.")

# Function to delete a player's score
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

# Function to start the game
def iniciar_jogo(player_initials):
    gamefile_path = 'gamefile copy 5.py'
    spec = importlib.util.spec_from_file_location("gamefile_copy_5", gamefile_path)
    gamefile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gamefile)

# Function to display the initial screen
def mostrar_tela_inicial():
    # Clear the initial window
    for widget in initial_window.winfo_children():
        widget.destroy()

    # Title of the main window
    title_label = tk.Label(initial_window, text="Bem-vindo ao jogo na Floresta!", font=custom_font_big, bg=VERDE, fg=BRANCO)
    title_label.pack(pady=20)

    # Button to view scores
    scores_button = tk.Button(initial_window, text="Ver Scores", font=custom_font_small, command=lambda: mostrar_scores(initial_window))
    scores_button.pack(pady=10)

    # Button to start the game
    start_button = tk.Button(initial_window, text="Iniciar Jogo", font=custom_font_small, command=lambda: iniciar_jogo(""))
    start_button.pack(pady=10)

    # Creating the options menu
    menu_bar = tk.Menu(initial_window)
    initial_window.config(menu=menu_bar)

    menu_opcoes = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Opções", menu=menu_opcoes)
    menu_opcoes.add_command(label="Adicionar Novo Jogador", command=lambda: adicionar_novo_jogador(initial_window))
    menu_opcoes.add_command(label="Excluir Pontuação", command=excluir_pontuacao)

# Main code
if __name__ == "__main__":
    # Creating the main window
    initial_window = tk.Tk()
    initial_window.title("Bem-vindo ao jogo na Floresta")

    # Styling the main window
    initial_window.configure(bg=VERDE)
    initial_window.geometry("600x400")

    # Loading the custom font
    custom_font_small = load_custom_font()
    custom_font_big = tkFont.Font(family="PixeloidMono", size=20)

    # Displaying the initial screen
    mostrar_tela_inicial()

    initial_window.mainloop()

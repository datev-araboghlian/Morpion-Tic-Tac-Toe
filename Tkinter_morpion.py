import tkinter as tk
from tkinter import messagebox
import random

# Global variables
case = {i: "" for i in range(1, 10)}
joueur_actuel = "X"
nombre_tour = 0
partie_en_cour = True
buttons = []
mode_de_jeu = "Humain"  # "Humain" or "IA"

# Function to display the game board in the GUI
def tableau():
    for i in range(1, 10):
        buttons[i-1].config(text=case[i], 
                            state="normal" if case[i] == "" else "disabled",
                            bg="white" if case[i] == "" else ("lightblue" if case[i] == "X" else "lightcoral"),
                            font=("Arial", 18, "bold"))

# Function to check if a player has won
def Condition_Pour_Gagner():
    victoire = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    for combinaison in victoire:
        if case[combinaison[0]] == case[combinaison[1]] == case[combinaison[2]] != "":
            return True
    return False

# Function to handle button clicks
def jouer(tour):
    global joueur_actuel, nombre_tour, partie_en_cour
    if not partie_en_cour or case[tour] != "":
        return
    
    # Update the board with the current player's move
    case[tour] = joueur_actuel
    tableau()
    
    # Check if the current player has won
    if Condition_Pour_Gagner():
        partie_en_cour = False
        # Use the 'after' method to delay the popup
        jeu_fenetre.after(500, lambda: messagebox.showinfo("Fin de la partie", f"Joueur {joueur_actuel} a gagné !"))
    elif nombre_tour == 8:  # 0 to 8 (9 turns) means all positions are filled
        partie_en_cour = False
        # Delay the message for draw
        jeu_fenetre.after(500, lambda: messagebox.showinfo("Fin de la partie", "Égalité"))
    else:
        # Switch players
        joueur_actuel = "O" if joueur_actuel == "X" else "X"
        nombre_tour += 1

        # If playing against the computer, let the AI play
        if mode_de_jeu == "IA" and joueur_actuel == "O":
            jouer_IA()

# AI move: choose a random available spot
def jouer_IA():
    global joueur_actuel, nombre_tour, partie_en_cour
    if not partie_en_cour:
        return
    
    # AI chooses a random available position
    available_positions = [i for i in range(1, 10) if case[i] == ""]
    if available_positions:
        ai_choice = random.choice(available_positions)
        case[ai_choice] = "O"
        tableau()
        
        # Check if the AI has won
        if Condition_Pour_Gagner():
            partie_en_cour = False
            jeu_fenetre.after(500, lambda: messagebox.showinfo("Fin de la partie", "L'IA a gagné !"))
        elif nombre_tour == 8:  # If all positions are filled, it's a draw
            partie_en_cour = False
            jeu_fenetre.after(500, lambda: messagebox.showinfo("Fin de la partie", "Égalité"))
        else:
            # Switch back to the human player
            joueur_actuel = "X"
            nombre_tour += 1

# Function to reset the game
def reset_game():
    global case, joueur_actuel, nombre_tour, partie_en_cour
    case = {i: "" for i in range(1, 10)}
    joueur_actuel = "X"
    nombre_tour = 0
    partie_en_cour = True
    tableau()

# Function to start the game with the selected mode
def start_game(mode):
    global mode_de_jeu
    mode_de_jeu = mode
    choix_fenetre.destroy()  # Close the selection window
    creer_fenetre_jeu()  # Create the game window

# Create the game window
def creer_fenetre_jeu():
    global buttons, jeu_fenetre
    jeu_fenetre = tk.Tk()
    jeu_fenetre.title("Morpion - Tic-Tac-Toe")
    jeu_fenetre.geometry("470x300")
    jeu_fenetre.configure(bg="lightgray")
    
    # Create buttons for the board
    buttons = []
    for i in range(1, 10):
        button = tk.Button(jeu_fenetre, text="", width=10, height=3, command=lambda i=i: jouer(i))
        button.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)
        buttons.append(button)

    # Add a reset button
    reset_button = tk.Button(jeu_fenetre, text="Réinitialiser", command=reset_game, bg="lightgreen", font=("Arial", 12, "bold"))
    reset_button.grid(row=3, column=0, columnspan=3, pady=10)

    # Initialize the board
    tableau()

# Create the initial window to choose game mode
choix_fenetre = tk.Tk()
choix_fenetre.title("Choisir le mode de jeu")
choix_fenetre.geometry("300x200")
choix_fenetre.configure(bg="lightgray")

# Add labels and buttons to choose the game mode
label = tk.Label(choix_fenetre, text="Avec qui voulez-vous jouer ?", font=("Arial", 14), bg="lightgray")
label.pack(pady=20)

mode_humain_button = tk.Button(choix_fenetre, text="Jouer contre un ami", command=lambda: start_game("Humain"), width=20, bg="lightblue", font=("Arial", 12))
mode_humain_button.pack(pady=10)

mode_ia_button = tk.Button(choix_fenetre, text="Jouer contre l'IA", command=lambda: start_game("IA"), width=20, bg="lightcoral", font=("Arial", 12))
mode_ia_button.pack(pady=10)

# Start the Tkinter event loop for the initial window
choix_fenetre.mainloop()



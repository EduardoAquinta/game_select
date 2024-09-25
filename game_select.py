import tkinter as tk
from tkinter import PhotoImage
import pygame
import os

# Initialize the controller and pygame
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(1)  # Use the first controller
joystick.init()

# Create a list of games and their paths
games = [
    {"name": "Mushihimisama", "path": "F:\SteamLibrary\steamapps\common\Mushihimesama\default.exe"},
    {"name": "Crimson Clover", "path": "F:\SteamLibrary\steamapps\common\Crimzon Clover World "
                                       "EXplosion\CrimzonCloverWEX.exe"},
    {"name": "DoDonPachi Resurrection", "path": "F:\SteamLibrary\steamapps\common\DoDonPachi Resurrection\default.exe"}
]


# Helper function to launch a game
def launch_game(game_path):
    os.startfile(game_path)


# Create a basic tkinter GUI
class GameLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Launcher")
        self.geometry("1024x800")

        # Load and display the background image
        self.bg_image = PhotoImage(file='dave.png')
        self.canvas = tk.Canvas(self, width=1024, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.selected_game = 0
        self.game_buttons = []

        # Define the button style (larger font and padding)
        button_style = {"font": ("Arial", 24), "padx": 20, "pady": 20}

        for i, game in enumerate(games):
            btn = tk.Button(self, text=game['name'], command=lambda g=game['path']: launch_game(g),
                            font=button_style["font"], padx=button_style["padx"], pady=button_style["pady"])
            self.game_buttons.append(btn)

        # Add buttons to the canvas at specific locations
        self.canvas.create_window(500, 300, window=self.game_buttons[0])
        self.canvas.create_window(500, 400, window=self.game_buttons[1])
        self.canvas.create_window(500, 500, window=self.game_buttons[2])

        # Highlight the first game initially
        self.highlight_selection()

        # Bind arrow keys for testing without controller
        self.bind('<Up>', self.move_up)
        self.bind('<Down>', self.move_down)
        self.bind('<Return>', self.select_game)

    # Highlight the currently selected game
    def highlight_selection(self):
        for i, btn in enumerate(self.game_buttons):
            if i == self.selected_game:
                btn.config(bg='red')
            else:
                btn.config(bg='SystemButtonFace')

    # Move selection up
    def move_up(self, event=None):
        if self.selected_game > 0:
            self.selected_game -= 1
        self.highlight_selection()

    # Move selection down
    def move_down(self, event=None):
        if self.selected_game < len(games) - 1:
            self.selected_game += 1
        self.highlight_selection()

    # Launch selected game
    def select_game(self, event=None):
        launch_game(games[self.selected_game]['path'])


# Controller polling
def handle_controller_input():
    pygame.event.pump()  # Process controller events
    if joystick.get_button(0):  # Assume button 0 is the "select" button
        app.select_game()
    if joystick.get_hat(0) == (0, 1):  # Up (Axis 1 negative)
        app.move_up()
    if joystick.get_hat(0) == (0, -1):  # Down (Axis 1 positive)
        app.move_down()

    # Re-run this function every 100ms
    app.after(100, handle_controller_input)


# Create and run the app
app = GameLauncher()
app.after(100, handle_controller_input)  # Start the controller input handling
app.mainloop()

# Quit pygame when done
pygame.quit()

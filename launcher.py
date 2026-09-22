# launcher.py
import customtkinter as ctk
import subprocess
import json
import os
import sys
from tkinter import messagebox

# -------------------------------
# CONFIGURATION
# -------------------------------
CONFIG_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "difficulty": "Normal",
    "speed": 1.0,
    "music": True,
    "high_score": 0
}

# -------------------------------
# SETTINGS HANDLER
# -------------------------------
def load_settings():
    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

settings = load_settings()

# -------------------------------
# MAIN APP WINDOW
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("🐍 Snake Game Hub")
app.geometry("600x480")
app.resizable(False, False)

# -------------------------------
# TITLE
# -------------------------------
title = ctk.CTkLabel(app, text="🐍 Snake Game Hub 🕹️",
                     font=("Segoe UI", 28, "bold"), text_color="#00FF99")
title.pack(pady=25)

subtitle = ctk.CTkLabel(app, text="Choose your play mode below",
                        font=("Segoe UI", 16))
subtitle.pack(pady=5)

# -------------------------------
# LAUNCH GAME FUNCTIONS
# -------------------------------
def launch_game(mode):
    try:
        if mode == "keyboard":
            subprocess.Popen([sys.executable, "snake_game.py"])
        elif mode == "gesture":
            subprocess.Popen([sys.executable, "gesture_control.py"])
        elif mode == "voice":
            subprocess.Popen([sys.executable, "voice_control.py"])
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------
# BUTTON STYLES
# -------------------------------
btn_style = {"font": ("Segoe UI", 16, "bold"), "corner_radius": 15, "height": 50}

frame = ctk.CTkFrame(app, corner_radius=20)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkButton(frame, text="🎮 Play with Keyboard", command=lambda: launch_game("keyboard"), **btn_style).pack(pady=12)
ctk.CTkButton(frame, text="🖐️ Play with Gesture", command=lambda: launch_game("gesture"), **btn_style).pack(pady=12)
ctk.CTkButton(frame, text="🎤 Play with Voice", command=lambda: launch_game("voice"), **btn_style).pack(pady=12)

# -------------------------------
# SETTINGS WINDOW
# -------------------------------
def open_settings():
    win = ctk.CTkToplevel(app)
    win.title("Settings ⚙️")
    win.geometry("400x400")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Settings", font=("Segoe UI", 22, "bold")).pack(pady=10)

    # Difficulty
    ctk.CTkLabel(win, text="Difficulty:").pack(pady=(20, 5))
    diff_var = ctk.StringVar(value=settings["difficulty"])
    ctk.CTkOptionMenu(win, variable=diff_var, values=["Easy", "Normal", "Hard"]).pack()

    # Speed
    ctk.CTkLabel(win, text="Game Speed:").pack(pady=(20, 5))
    speed_slider = ctk.CTkSlider(win, from_=0.5, to=2.0, number_of_steps=6)
    speed_slider.set(settings["speed"])
    speed_slider.pack(padx=20)

    # Music toggle
    music_var = ctk.BooleanVar(value=settings["music"])
    ctk.CTkSwitch(win, text="Enable Music", variable=music_var).pack(pady=20)

    def save():
        settings["difficulty"] = diff_var.get()
        settings["speed"] = round(speed_slider.get(), 2)
        settings["music"] = music_var.get()
        save_settings(settings)
        messagebox.showinfo("Saved", "Settings updated successfully!")
        win.destroy()

    ctk.CTkButton(win, text="Save", command=save, fg_color="#00FF99", hover_color="#009966").pack(pady=20)

# -------------------------------
# ABOUT WINDOW
# -------------------------------
def about_window():
    win = ctk.CTkToplevel(app)
    win.title("About ℹ️")
    win.geometry("420x300")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="About Snake Game Hub", font=("Segoe UI", 20, "bold")).pack(pady=15)
    ctk.CTkLabel(win, text="Created by Shahan Samar 👨‍💻\n\nPlay Snake in 3 modes:\n• Keyboard\n• Gesture (Webcam)\n• Voice Commands\n\nBuilt with Python 🐍 & CustomTkinter 💻",
                 justify="center", wraplength=380, font=("Segoe UI", 14)).pack(pady=15)

# -------------------------------
# EXTRA BUTTONS
# -------------------------------
footer = ctk.CTkFrame(app)
footer.pack(pady=10)

ctk.CTkButton(footer, text="⚙️ Settings", command=open_settings, width=120).grid(row=0, column=0, padx=10)
ctk.CTkButton(footer, text="🏆 High Score", width=120,
              command=lambda: messagebox.showinfo("High Score", f"Your highest score: {settings['high_score']}")).grid(row=0, column=1, padx=10)
ctk.CTkButton(footer, text="ℹ️ About", command=about_window, width=120).grid(row=0, column=2, padx=10)

# -------------------------------
# EXIT BUTTON
# -------------------------------
ctk.CTkButton(app, text="❌ Exit", command=app.destroy,
              fg_color="#ff3b3b", hover_color="#b30000", width=200).pack(pady=10)

# -------------------------------
# ANIMATION (FADE IN)
# -------------------------------
app.attributes('-alpha', 0.0)
def fade_in(alpha=0): 
    if alpha < 1:
        alpha += 0.05
        app.attributes('-alpha', alpha)
        app.after(50, fade_in, alpha)
fade_in()

app.mainloop()

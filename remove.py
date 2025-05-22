import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from rembg import remove
import os

# --- THEME SETTINGS ---
current_theme = "light"
font_family = "Times New Roman"
icon_path = "app_icon.ico"  # You can place your own icon here

themes = {
    "light": {
        "bg": "#f5f5f5",
        "fg": "#222222",
        "button_bg": "#4a90e2",
        "button_fg": "white"
    },
    "dark": {
        "bg": "#2b2b2b",
        "fg": "#ffffff",
        "button_bg": "#444444",
        "button_fg": "#00ffff"
    }
}

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

def apply_theme():
    theme = themes[current_theme]
    window.configure(bg=theme["bg"])
    title_label.config(bg=theme["bg"], fg=theme["fg"], font=(font_family, 16, "bold"))
    input_label.config(bg=theme["bg"], fg=theme["fg"], font=(font_family, 10))
    select_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    theme_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    progress_label.config(bg=theme["bg"], fg=theme["fg"], font=(font_family, 9))

# Process selected files and save to folder
def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if file_paths:
        input_label.config(text=f"{len(file_paths)} file(s) selected.")
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if output_folder:
            process_all_images(file_paths, output_folder)

# Remove background from all images
def process_all_images(file_list, output_folder):
    total = len(file_list)
    for index, path in enumerate(file_list):
        process_image(path, output_folder)
        progress["value"] = (index + 1) / total * 100
        progress_label.config(text=f"{index + 1} of {total} processed.")
        window.update_idletasks()

    messagebox.showinfo("Done", f"All images processed successfully.\nSaved to:\n{output_folder}")
    reset_ui()

def process_image(input_path, output_folder):
    try:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_folder, f"{file_name}_no_bg.png")

        with open(input_path, "rb") as i:
            input_data = i.read()
            output_data = remove(input_data)
            with open(output_path, "wb") as o:
                o.write(output_data)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Reset UI elements after processing
def reset_ui():
    input_label.config(text="No files selected.")
    progress["value"] = 0
    progress_label.config(text="")

# Handle drag & drop (Windows only)
def drop(event):
    files = window.tk.splitlist(event.data)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if image_files:
        input_label.config(text=f"{len(image_files)} file(s) dropped.")
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if output_folder:
            process_all_images(image_files, output_folder)

# --- GUI SETUP ---
window = tk.Tk()
window.title("Background Remover Pro")
window.geometry("550x380")
window.resizable(False, False)

# Set icon
try:
    window.iconbitmap(icon_path)
except:
    pass

# Enable drag & drop (Windows)
try:
    window.tk.call('tk', 'windowingsystem')
    window.drop_target_register(DND_FILES := 'DND_Files')
    window.dnd_bind('<<Drop>>', drop)
except:
    pass

# Title
title_label = tk.Label(window, text="Image Background Remover")
title_label.pack(pady=15)

# File info label
input_label = tk.Label(window, text="No files selected.", wraplength=500, justify="center")
input_label.pack(pady=5)

# Select file button
select_button = tk.Button(window, text="Select Images & Folder", command=select_files, padx=20, pady=8)
select_button.pack(pady=10)

# Theme switch
theme_button = tk.Button(window, text="Toggle Light/Dark Theme", command=toggle_theme, padx=15, pady=6)
theme_button.pack(pady=5)

# Progress bar
progress = ttk.Progressbar(window, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=15)

# Progress label
progress_label = tk.Label(window, text="", justify="center")
progress_label.pack()

# Apply theme
apply_theme()

# Run app
window.mainloop()

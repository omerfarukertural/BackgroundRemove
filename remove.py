import tkinter as tk
from tkinter import filedialog, messagebox, ttk, StringVar, colorchooser
from rembg import remove
from PIL import Image, ImageTk, ImageEnhance
import os
import io
import json
import datetime

try:
    import tkinterdnd2 as tkdnd
    TKDND_AVAILABLE = True
except ImportError:
    TKDND_AVAILABLE = False

current_theme = "light"
font_family = "Segoe UI"
icon_path = "app_icon.ico"
current_lang = "en"
log_file = "processing_log.txt"
preview_image = None
cancel_requested = False
CONFIG_PATH = "config.json"
background_fill_color = (255, 255, 255, 255)
resize_width, resize_height = 0, 0

languages = {
    "en": {
        "title": "Image Background Remover",
        "select_images": "Select Images",
        "toggle_theme": "Toggle Theme",
        "select_format": "Output Format:",
        "file_selected": "file(s) selected.",
        "done": "All images processed successfully.\nSaved to:\n",
        "error": "An error occurred:",
        "no_files": "No files selected.",
        "processed": "processed.",
        "open_folder": "Open Output Folder",
        "cancel": "Cancel",
        "lang_toggle": "TR / EN",
        "preview": "Preview",
        "original": "Original",
        "result": "Result",
        "set_bg": "Set BG Color"
    },
    "tr": {
        "title": "Görsel Arka Plan Kaldırıcı",
        "select_images": "Görselleri Seç",
        "toggle_theme": "Tema Değiştir",
        "select_format": "Çıktı Formatı:",
        "file_selected": "adet dosya seçildi.",
        "done": "Tüm görseller başarıyla işlendi.\nKayıt yeri:\n",
        "error": "Bir hata oluştu:",
        "no_files": "Dosya seçilmedi.",
        "processed": "işlendi.",
        "open_folder": "Klasörü Aç",
        "cancel": "İptal",
        "lang_toggle": "EN / TR",
        "preview": "Önizleme",
        "original": "Orijinal",
        "result": "Sonuç",
        "set_bg": "Arka Plan Rengi"
    }
}

themes = {
    "light": {"bg": "#f0f4f8", "fg": "#1e293b", "button_bg": "#2563eb", "button_fg": "white"},
    "dark": {"bg": "#1e293b", "fg": "#f0f4f8", "button_bg": "#334155", "button_fg": "#facc15"}
}

def get_text(key):
    return languages[current_lang][key]

def toggle_language():
    global current_lang
    current_lang = "tr" if current_lang == "en" else "en"
    update_labels()

def update_labels():
    window.title(get_text("title"))
    label_title.config(text=get_text("title"))
    label_file.config(text=get_text("no_files"))
    format_label.config(text=get_text("select_format"))
    button_select.config(text=get_text("select_images"))
    theme_button.config(text=get_text("toggle_theme"))
    lang_button.config(text=get_text("lang_toggle"))
    color_button.config(text=get_text("set_bg"))
    original_label.config(text=get_text("original"))
    result_label.config(text=get_text("result"))

def choose_color():
    global background_fill_color
    color = colorchooser.askcolor()[0]
    if color:
        background_fill_color = tuple(map(int, color)) + (255,)

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()
    update_labels()

def apply_theme():
    style = ttk.Style()
    theme = themes[current_theme]
    window.configure(bg=theme["bg"])
    style.theme_use('default')
    style.configure("TProgressbar", troughcolor=theme["bg"], background=theme["button_bg"], bordercolor=theme["bg"], lightcolor=theme["button_bg"], darkcolor=theme["button_bg"])
    for widget in [label_title, label_file, format_label, original_label, result_label, progress_label]:
        widget.configure(bg=theme["bg"], fg=theme["fg"])
    try:
        for button in [button_select, theme_button, lang_button, color_button]:
            button.configure(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["button_bg"], activeforeground=theme["button_fg"], relief="raised")
    except NameError:
        pass

def enhance_image(img):
    enhancer_brightness = ImageEnhance.Brightness(img)
    enhancer_contrast = ImageEnhance.Contrast(img)
    img = enhancer_brightness.enhance(1.05)
    img = enhancer_contrast.enhance(1.1)
    return img

window = tk.Tk()
window.title(get_text("title"))
window.geometry("420x640")
window.resizable(False, False)

try:
    window.iconbitmap(icon_path)
except:
    pass

label_title = tk.Label(window, text=get_text("title"), font=(font_family, 18, "bold"), anchor="center")
label_title.grid(row=0, column=0, columnspan=3, pady=10)

label_file = tk.Label(window, text=get_text("no_files"), font=(font_family, 12), anchor="center")
label_file.grid(row=1, column=0, columnspan=3, pady=(0, 10))

format_label = tk.Label(window, text=get_text("select_format"), font=(font_family, 12), anchor="center")
format_label.grid(row=3, column=0, columnspan=3, pady=(10, 2))

output_format = StringVar(value="png")
format_dropdown = ttk.Combobox(window, textvariable=output_format, values=["png", "jpg", "webp", "bmp", "tiff"], state="readonly")
format_dropdown.grid(row=4, column=0, columnspan=3, pady=(0, 10))

original_label = tk.Label(window, text=get_text("original"), font=(font_family, 12, "bold"), anchor="center")
original_label.grid(row=5, column=0)

result_label = tk.Label(window, text=get_text("result"), font=(font_family, 12, "bold"), anchor="center")
result_label.grid(row=5, column=2)

canvas_original = tk.Canvas(window, width=180, height=180, bg="white", highlightthickness=2, highlightbackground="#999999")
canvas_original.grid(row=6, column=0, padx=10, pady=(0, 10))

canvas_result = tk.Canvas(window, width=180, height=180, bg="white", highlightthickness=2, highlightbackground="#999999")
canvas_result.grid(row=6, column=2, padx=10, pady=(0, 10))

progress = ttk.Progressbar(window, orient="horizontal", length=360, mode="determinate")
progress.grid(row=7, column=0, columnspan=3, pady=15)

progress_label = tk.Label(window, text="", font=(font_family, 10, "italic"))
progress_label.grid(row=8, column=0, columnspan=3)

theme_button = tk.Button(window, text=get_text("toggle_theme"), command=toggle_theme, compound="left")
theme_icon = ImageTk.PhotoImage(Image.open("iconstheme.png").resize((16, 16)))
theme_button.config(image=theme_icon)
theme_button.image = theme_icon
theme_button.grid(row=9, column=0, pady=10, padx=10, sticky="e")

lang_button = tk.Button(window, text=get_text("lang_toggle"), command=toggle_language, compound="left")
lang_icon = ImageTk.PhotoImage(Image.open("iconslang.png").resize((16, 16)))
lang_button.config(image=lang_icon)
lang_button.image = lang_icon
lang_button.grid(row=9, column=2, pady=10, padx=10, sticky="w")

color_button = tk.Button(window, text=get_text("set_bg"), command=choose_color, compound="left")
color_icon = ImageTk.PhotoImage(Image.open("iconscolor.png").resize((16, 16)))
color_button.config(image=color_icon)
color_button.image = color_icon
color_button.grid(row=10, column=0, columnspan=3, pady=5)

def reset_ui():
    label_file.config(text=get_text("no_files"))
    progress["value"] = 0
    progress_label.config(text="")
    canvas_original.delete("all")
    canvas_result.delete("all")

def preview_first_image(path):
    global preview_image
    try:
        img_orig = Image.open(path)
        img_orig.thumbnail((180, 180))
        preview_orig = ImageTk.PhotoImage(img_orig)
        canvas_original.delete("all")
        canvas_original.create_image(90, 90, image=preview_orig)
        canvas_original.image = preview_orig

        with open(path, "rb") as f:
            data = f.read()
        removed = remove(data)
        img_proc = Image.open(io.BytesIO(removed)).convert("RGBA")
        bg = Image.new("RGBA", img_proc.size, background_fill_color)
        combined = Image.alpha_composite(bg, img_proc)
        combined = enhance_image(combined)
        combined.thumbnail((180, 180))
        preview_proc = ImageTk.PhotoImage(combined)
        canvas_result.delete("all")
        canvas_result.create_image(90, 90, image=preview_proc)
        canvas_result.image = preview_proc
    except Exception as e:
        messagebox.showerror("Error", f"{get_text('error')}: {e}")

def process_image(input_path, output_folder):
    try:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        out_ext = output_format.get()
        output_path = os.path.join(output_folder, f"{file_name}_no_bg.{out_ext}")

        with open(input_path, "rb") as i:
            input_data = i.read()
            output_data = remove(input_data)
            result_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
            background = Image.new("RGBA", result_image.size, background_fill_color)
            composite = Image.alpha_composite(background, result_image)
            composite = enhance_image(composite)
            composite = composite.convert("RGB") if out_ext != "png" else composite
            composite.save(output_path)
    except Exception as e:
        messagebox.showerror("Error", f"{get_text('error')}: {e}")

def process_all_images(file_list, output_folder):
    def animate():
        dots = ['   ', '.  ', '.. ', '...']
        idx = 0
        def step():
            nonlocal idx
            if cancel_requested:
                return
            progress_label.config(text=f"{get_text('processed')} {dots[idx % 4]}")
            idx += 1
            window.after(300, step)
        step()
    animate()
    total = len(file_list)
    for index, path in enumerate(file_list):
        process_image(path, output_folder)
        progress["value"] = (index + 1) / total * 100
        progress_label.config(text=f"{index + 1} / {total} {get_text('processed')}")
        window.update_idletasks()
    messagebox.showinfo("Done", f"{get_text('done')}{output_folder}")
    reset_ui()

def select_files():
    file_paths = filedialog.askopenfilenames(
        title=get_text("select_images"),
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if file_paths:
        label_file.config(text=f"{len(file_paths)} {get_text('file_selected')}")
        output_folder = filedialog.askdirectory(title=get_text("open_folder"))
        if output_folder:
            preview_first_image(file_paths[0])
            process_all_images(file_paths, output_folder)

button_select = tk.Button(window, text=get_text("select_images"), command=select_files, compound="left")
select_icon = ImageTk.PhotoImage(Image.open("iconsselect.png").resize((16, 16)))
button_select.config(image=select_icon)
button_select.image = select_icon
button_select.grid(row=2, column=0, columnspan=3, pady=10)

window.update_idletasks()
apply_theme()

window.mainloop()

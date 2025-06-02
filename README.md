Background Remover Pro
A clean, minimal desktop application built with Python and Tkinter to remove
backgrounds from images using rembg. The app supports drag-and-drop, batch
processing, light/dark themes, multi-format outputs, language toggle (EN/TR),
and more.
Features
- Clean & Minimal GUI
Built entirely with Tkinter for a lightweight, responsive interface.
- Light / Dark Theme Toggle
Instantly switch between light and dark modes for comfortable use in any
environment.
- English / Turkish Language Support
All labels, buttons, and window titles update when you toggle between English
and Turkish.
- Drag & Drop & Multi-Select
Drag one or more images into the window, or click “Select Images” to choose
multiple files at once.
- Batch Processing & Multi-Format Output
Remove backgrounds from dozens of images in one go. Save results as PNG, JPG,
WEBP, BMP, or TIFF.
- Background Color Picker
Instead of a transparent background, choose a solid color (white, gray, or any
custom RGB) to fill behind your subject.
- Live Progress Bar & Animated Status
Visual feedback shows how many files have been processed, plus a simple dot
animation during conversion.
- Before / After Previews
See the “Original” image on the left and the “Result” on the right, with the
background removed, color fill, and enhancements.
- Post-Processing UI Reset
When processing completes, the app automatically clears previews and resets
all controls—ready for another batch.
- Built-In Image Enhancements
Automatically boost brightness by 5% and contrast by 10% on each exported
image for a polished, professional look.
- Custom Styling
Refined font sizes, layout adjustments, and consistent colors make the UI feel
cohesive and modern.
Screenshots
Include your own screenshot in the screenshots folder.
Requirements
- Python 3.9+
- rembg
- Pillow
- tkinter (bundled with Python)
- tkinterdnd2 (optional, for drag-and-drop on Windows)
Install dependencies with:
pip install rembg pillow tkinterdnd2
Getting Started
1. Clone the repository:
git clone https://github.com/your-username/BackgroundRemoverPro.git
cd BackgroundRemoverPro
2. Install requirements:
pip install rembg pillow tkinterdnd2
3. Run the app:
python remove.py
How It Works
1. Select or Drag & Drop
- Click the “Select Images” button or drag image files (.png, .jpg, .jpeg)
into the window.
2. Choose an Output Folder
- Pick where you want the processed images saved.
3. Process & Preview
- The left preview shows the original image; the right preview shows the
image with the background removed, color-filled, and enhanced.
- Watch the progress bar and animated status as each image is processed.
4. Background Color & Theme
- Click “Set BG Color” to choose a solid fill behind the subject.
- Toggle “Light / Dark” to switch themes.
5. Language Switching
- Click “TR / EN” to swap all labels, buttons, and window title between
Turkish and English.
6. Batch Export
- Each processed file is saved with a suffix _no_bg and your chosen format
(PNG, JPG, WEBP, BMP, TIFF).
7. Automatic Reset
- After processing, the previews clear, the file count resets, and the
progress bar resets—ready for a new batch.
Project Structure
BackgroundRemoverPro/
nnn icons/ # 16×16 PNG icons: select.png, theme.png, lang.png,
color.png
nnn screenshots/ # Store your screenshots here (e.g. app_screenshot.png)
nnn remove.py # Main application script
nnn config.json # (auto-created) Stores user preferences: theme, language,
BG color
nnn processing_log.txt # (auto-created) Logs processed output file paths
nnn README.md # This file
Future Plans
- Export as .exe with Custom Icon
- Advanced Size Optimization
- Auto-Open Output Folder
- Additional Language Support
- Customizable Image Enhancements (sliders for brightness/contrast)
License
This project is released under the MIT License – free for personal and
commercial use.
Acknowledgments
- rembg – for the background removal engine powered by U-2-Net.
- Tkinter – for the simple, cross-platform GUI framework.
- Python Community – all the open source libraries and helpers that make this
possible.

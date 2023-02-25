from PIL import Image
import pytesseract
import json

# to browse for a file on your computer or mobile device using the built-in tkinter library
# tkinter is a GUI library, so this program requires a graphical user interface to be present
import tkinter as tk
from tkinter import filedialog
import os


import fitz



root = tk.Tk()
root.withdraw()


print("Please choose the file")

file_path = filedialog.askopenfilename()
file_name = os.path.basename(file_path)
print("Selected file name:", file_name)

text_list = []


# Folder where tesseract is installed
# This is required only for Windows machine 
# Please comment this line if you run on different machine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
    # The selected file is an image, so load it as a PIL image object
    pages = [Image.open(file_path)]

    # Loop through each page and perform OCR
    for page in pages:
        # Perform OCR on the page
        text = pytesseract.image_to_string(page)
        # Append extracted text to the list
        text_list.append(text)


elif file_name.lower().endswith(('.pdf')):
    # txt = []
    doc = fitz.open(file_path)            # some existing PDF
    for page in doc:
        text = page.get_text("text")
        text = text.split('\n')
        text_list.extend(text)
 
# Convert to JSON
data = {'text': text_list}
json_data = json.dumps(data,indent=4)


# Write the JSON data to a file
with open('file_output.json', 'w') as f:
    f.write(json_data)
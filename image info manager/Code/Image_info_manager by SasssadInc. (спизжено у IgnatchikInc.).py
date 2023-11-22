from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image

selected_image_path = ""
diag = 13

def get_folder():
    filepath = filedialog.askdirectory()
    folder_path.delete(0, END)
    folder_path.insert(INSERT, filepath)
    tree.delete(*tree.get_children())
    scan(filepath)

def image_info(image_path):
    img = Image.open(image_path)
    name = os.path.basename(image_path)
    width, height = img.size
    resolution = (width**2 + height**2)**(1/2) / diag
    depth = img.mode
    compression = img.info.get("compression", "N/A")
    entropy = '%.3f'%img.entropy()

    return name, str(width) + 'x' + str(height), resolution, depth, compression, entropy

def scan(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.jpg', '.gif', '.tif', '.bmp', '.png', '.pcx')):
                tree.insert("", END, values=image_info(os.path.join(root, file)))

def show_image(event):
    global selected_image_path
    selected_item = tree.item(tree.selection())
    image_name = selected_item['values'][0]
    selected_image_path = os.path.join(folder_path.get(), image_name)
    img = Image.open(selected_image_path)
    img.show()


root = Tk()
root.iconbitmap(default="icon.ico")
root.title("Image Info")
root.geometry('600x650')
root.configure(bg='black')  # Set background color to black

# Create a custom font style
custom_font = ("Courier New", 12, "bold")

# Update folder path entry widget
folder_path = Entry(root, width=50, bg='darkgray', font=custom_font, foreground='#FF69B4')
folder_path.grid(row=0, column=0, padx=20, pady=20, sticky=(W, E))

# Update "Choose Folder" button
btn_folder_path = Button(root, text="Choose Folder", command=get_folder, width=20, bg='#FF69B4', font=custom_font, foreground='#000000')
btn_folder_path.grid(row=0, column=1, padx=20, pady=20, sticky=(W, E))

columns = ('Name', 'Size', 'Dots/Inch', 'Color Depth', 'Compression', "Entropy")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=1, columnspan=2, sticky=(N, S, W, E))

# Update treeview styles
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=custom_font, rowheight=25, background='black', foreground='#FF69B4')
style.configure("Treeview.Heading", font=custom_font, background='black', foreground='#FF69B4')

# Update treeview headings
tree.heading("Name", text="Name", anchor=CENTER)
tree.heading("Size", text="Size", anchor=CENTER)
tree.heading("Dots/Inch", text="Dots/Inch", anchor=CENTER)
tree.heading("Color Depth", text="Color Depth", anchor=CENTER)
tree.heading("Compression", text="Compression", anchor=CENTER)
tree.heading("Entropy", text="Entropy", anchor=CENTER)

# Update scrollbar style
scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=2, sticky=(N, S, W, E))

# Bind the show_image function
tree.bind("<<TreeviewSelect>>", show_image)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Add "Dead Inside" text
dead_inside_label = Label(root, text="Dead Inside", font=("Helvetica", 24, "bold"), fg="white", bg="black")
dead_inside_label.place(relx=0.5, rely=0.9, anchor=CENTER)

root.mainloop()
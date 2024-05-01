import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, Image, ImageTk


class Ui_MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paint App")
        self.root.wm_iconbitmap(r"img\pencil.ico")
        self.root.state('zoomed')
        self.root.config(bg="#18181b")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # LEFT MENU
        frame_menu = tk.Frame(self.root, bg="#09090b")
        frame_menu.grid(row=0, column=0, sticky='nsew')

        self.pen_img = ImageTk.PhotoImage(Image.open(r"img\pencil.png").resize((25, 25), Image.LANCZOS))
        self.pen_button = tk.Button(frame_menu, image=self.pen_img)
        self.pen_button.grid(row=0, column=0)

        # self.fill_img = ImageTk.PhotoImage(Image.open(r"img\fill.png").resize((25, 25), Image.LANCZOS))
        # self.fill_button = tk.Button(frame_menu, image=self.fill_img)
        # self.fill_button.grid(row=1, column=0)

        self.eraser_img = ImageTk.PhotoImage(Image.open(r"img\eraser.png").resize((25, 25), Image.LANCZOS))
        self.eraser_button = tk.Button(frame_menu, image=self.eraser_img)
        self.eraser_button.grid(row=2, column=0)

        self.color_img = ImageTk.PhotoImage(Image.open(r"img\wheel.png").resize((25, 25), Image.LANCZOS))
        self.color_button = tk.Button(frame_menu, image=self.color_img)
        self.color_button.grid(row=3, column=0)
        
        self.square_img = ImageTk.PhotoImage(Image.open(r"img\square.png").resize((25, 25), Image.LANCZOS))
        self.square_button = tk.Button(frame_menu, image=self.square_img)
        self.square_button.grid(row=4, column=0)

        self.triangle_img = ImageTk.PhotoImage(Image.open(r"img\triangle.png").resize((25, 25), Image.LANCZOS))
        self.triangle_button = tk.Button(frame_menu, image=self.triangle_img)
        self.triangle_button.grid(row=5, column=0)

        self.circle_img = ImageTk.PhotoImage(Image.open(r"img\circle.png").resize((25, 25), Image.LANCZOS))
        self.circle_button = tk.Button(frame_menu, image=self.circle_img)
        self.circle_button.grid(row=6, column=0)


        style = ttk.Style()

        # Стиль вкладок
        style.theme_create("NotebookStyle", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "background": "#18181b"
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [10, 5],
                    "background": "#09090b",
                    "foreground": "#fff"
                },
                "map": {
                    "background": [("selected", "#6cb8e6")],
                }
            }
        })
        style.theme_use("NotebookStyle")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=1, sticky='nsew')


class Tab:
    def __init__(self, root, title, w, h):
        self.root = root
        self.title = title
        self.w, self.h = w, h

    def new_tab(self):
        tab = tk.Frame(self.root, background="#18181b")
        self.root.add(tab, text=self.title)

        tab_cont = tk.Frame(tab, bg="#18181b")
        tab_cont.pack(expand=True)

        self.drawing_area = tk.Canvas(tab_cont, width=self.w, height=self.h, bg="#fff")
        self.drawing_area.pack()
        return self.drawing_area

class NewDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create Dialog")


        self.frame_title = tk.Frame(self.dialog)
        self.frame_title.pack()

        self.label = tk.Label(self.frame_title, text="Title:")
        self.label.pack(side=tk.LEFT, pady=10)
        self.title = tk.Entry(self.frame_title)
        self.title.pack(side=tk.RIGHT, pady=5)


        self.frame_width = tk.Frame(self.dialog)
        self.frame_width.pack()
        
        self.label = tk.Label(self.frame_width, text="W px:")
        self.label.pack(side=tk.LEFT, pady=10)
        self.width = tk.Entry(self.frame_width)
        self.width.insert(0, 1024)
        self.width.pack(side=tk.RIGHT, pady=5)


        self.frame_heighth = tk.Frame(self.dialog)
        self.frame_heighth.pack()

        self.label = tk.Label(self.frame_heighth, text="H px:")
        self.label.pack(side=tk.LEFT, pady=10)
        self.height = tk.Entry(self.frame_heighth)
        self.height.insert(0, 512)
        self.height.pack(side=tk.RIGHT, pady=5)


        self.frame_bottom = tk.Frame(self.dialog)
        self.frame_bottom.pack()

        self.ok_button = tk.Button(self.frame_bottom, text="OK", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = tk.Button(self.frame_bottom, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side=tk.RIGHT, padx=10)

        self.title.focus_set()
        self.result = None

    def on_ok(self):
        self.result = {"title": self.title.get(), "w": self.width.get(), "h": self.height.get()}
        self.dialog.destroy()

    def on_cancel(self):
        self.result = None
        self.dialog.destroy()

class SizeDialog:
    def __init__(self, parent, title, default):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"{title} Size")


        self.frame_width = tk.Frame(self.dialog)
        self.frame_width.pack()

        self.label = tk.Label(self.frame_width, text="W px:")
        self.label.pack(side=tk.LEFT, pady=10)
        self.width = tk.Entry(self.frame_width)
        self.width.insert(0, default)
        self.width.pack(side=tk.RIGHT, pady=5)


        self.frame_bottom = tk.Frame(self.dialog)
        self.frame_bottom.pack()

        self.ok_button = tk.Button(self.frame_bottom, text="OK", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = tk.Button(self.frame_bottom, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side=tk.RIGHT, padx=10)

        self.width.focus_set()
        self.result = None

    def on_ok(self):
        self.result = {"w": self.width.get()}
        self.dialog.destroy()

    def on_cancel(self):
        self.result = None
        self.dialog.destroy()
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser, filedialog, simpledialog
from design import Ui_MainWindow, Tab, NewDialog, SizeDialog
from tools import ToolSettings
from PIL import ImageGrab, Image, ImageTk

import os

class MainWindow:
    def __init__(self):
        self.ui = Ui_MainWindow()
        self.root = self.ui.root
        self.tool_settings = ToolSettings()

        self.current_tab = None

        menubar = tk.Menu(self.root)
        menubar.config(bg="#000")
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False, background="#09090b", foreground="#fff", border=0)
        menubar.add_cascade(menu=file_menu, label="File"),
        self.openBtn = file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.load_image)
        self.newBtn = file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_tab)
        self.saveBtn = file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_image)
        self.clearBtn = file_menu.add_command(label="Clear", accelerator="Ctrl+L", command=self.clear)
        self.outBtn = file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.root.quit)

        self.ui.pen_button.config(command=self.set_tool_pen)

        self.ui.square_button.config(command=self.set_tool_square)
        self.ui.triangle_button.config(command=self.set_tool_triangle)
        self.ui.circle_button.config(command=self.set_tool_circle)

        self.ui.eraser_button.config(command=self.set_tool_eraser)

        self.ui.color_button.config(command=self.change_color)


        self.setup_tools()
        self.setup_bindings()
        self.root.mainloop()

    def setup_tools(self):
        self.tool_settings.tool = "pen"
        self.tool_settings.color = "#000"

        self.start_x, self.start_y = None, None

        self.shape_id = None
        self.image = None
        self.image_id = None

    def setup_cursor(self):
        if self.is_cursor_inside(self.current_tab):
            if self.tool_settings.tool == "pen":
                self.current_tab.config(cursor="cross")
            elif self.tool_settings.tool == "eraser":
                self.current_tab.config(cursor="circle")
        if self.tool_settings.tool in ["pen", "square", "triangle", "circle"]:
            self.current_tab.bind("<Enter>", lambda event: self.current_tab.config(cursor="cross"))
            self.current_tab.bind("<Leave>", lambda event: self.current_tab.config(cursor=""))
        elif self.tool_settings.tool == "eraser":
            self.current_tab.bind("<Enter>", lambda event: self.current_tab.config(cursor="circle"))
            self.current_tab.bind("<Leave>", lambda event: self.current_tab.config(cursor=""))


    def new_tab(self):
        dialog = NewDialog(self.root)
        self.root.wait_window(dialog.dialog)

        if dialog.result is not None:
            self.t = Tab(self.ui.notebook, dialog.result["title"], dialog.result["w"], dialog.result["h"]).new_tab()
            self.current_tab = self.t
            self.set_current_tab()
            self.setup_cursor()
            self.setup_draw_bindings()

    def set_current_tab(self):
        last_tab_index = self.ui.notebook.index('end') - 1
        self.ui.notebook.select(last_tab_index)

    def change_tab(self, event):
        selected_tab = event.widget.select()
        current_tab_index = event.widget.index(selected_tab)
        current_tab_frame = event.widget.winfo_children()[current_tab_index]
        self.current_tab = current_tab_frame.winfo_children()[0].winfo_children()[0]

    def keys(self, event):
        if event.keycode == 78:
            self.new_tab()
        elif event.keycode == 81:
            self.root.quit()
    def setup_bindings(self):
        self.ui.notebook.bind("<ButtonRelease-1>", self.change_tab)
        self.root.bind("<Control-KeyPress>", self.keys)
        self.root.bind("<KeyPress>", self.keys)

    def draw_keys(self, event):
        if event.keycode == 79:
            self.load_image()
        elif event.keycode == 83:
            self.save_image()
        elif event.keycode == 76:
            self.clear()
        if event.keycode == 66:
            self.set_tool_pen()
            self.setup_cursor()
        elif event.keycode == 69:
            self.set_tool_eraser()
            self.setup_cursor()
    def setup_draw_bindings(self):
        self.root.bind("<Control-KeyPress>", self.draw_keys)
        self.root.bind("<KeyPress>", self.draw_keys)

        if self.tool_settings.tool not in ["square", "triangle", "circle"]:
            self.current_tab.bind("<Button-1>", self.paint_dot)
            self.current_tab.bind("<B1-Motion>", self.paint)
            self.current_tab.bind("<ButtonRelease-1>", self.reset)
            self.current_tab.bind("<Button-3>", self.change_size)
        else:
            self.current_tab.unbind("<B1-Motion>")
            self.current_tab.bind("<Button-1>", self.figures)
            self.current_tab.bind("<ButtonRelease-1>", self.figures_reset)


    def paint_dot(self, event):
        x, y = event.x, event.y
        if self.tool_settings.tool == "pen":
            self.current_tab.create_oval(x-(self.tool_settings.pen_size / 2), y-(self.tool_settings.pen_size / 2), x+(self.tool_settings.pen_size / 2), y+(self.tool_settings.pen_size / 2), fill=self.tool_settings.color, outline=self.tool_settings.color)
        elif self.tool_settings.tool == "eraser":
            self.current_tab.create_oval(x-(self.tool_settings.eraser_size / 2), y-(self.tool_settings.eraser_size / 2), x+(self.tool_settings.eraser_size / 2), y+(self.tool_settings.eraser_size / 2), fill="#fff", outline="#fff")

    def paint(self, event):
        x, y = event.x, event.y
        if self.start_x and self.start_y:
            if self.tool_settings.tool == "pen":
                self.current_tab.create_line(self.start_x, self.start_y, x, y, capstyle=tk.ROUND, smooth=True, splinesteps=36, width=self.tool_settings.pen_size, fill=self.tool_settings.color)
            elif self.tool_settings.tool == "eraser":
                self.current_tab.create_line(self.start_x, self.start_y, x, y, capstyle=tk.ROUND, smooth=True, splinesteps=36, width=self.tool_settings.eraser_size, fill="#fff")
        self.start_x, self.start_y = x, y
    def reset(self, event):
        self.start_x, self.start_y = None, None


    def figures(self, event):
        self.start_x, self.start_y = event.x, event.y
        
    def figures_reset(self, event):
        x, y = event.x, event.y
        if self.tool_settings.tool == "square":
            self.current_tab.create_rectangle(self.start_x, self.start_y, x, y, width=self.tool_settings.figure_size, outline=self.tool_settings.color)
        if self.tool_settings.tool == "triangle":
            self.create_triangle(self.current_tab, self.start_x, self.start_y, x, y, width=self.tool_settings.figure_size, outline=self.tool_settings.color)
        elif self.tool_settings.tool == "circle":
            self.current_tab.create_oval(self.start_x, self.start_y, x, y, width=self.tool_settings.figure_size, outline=self.tool_settings.color)
        self.start_x, self.start_y = None, None


    def create_triangle(self, canvas, sx, sy, ex, ey, width, outline):
        x1, y1 = sx, ey
        x2, y2 = ((sx + ex) / 2), sy
        x3, y3 = ex, ey
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, width=width, outline=outline)

    def set_tool_pen(self):
        self.tool_settings.tool = "pen"
        self.setup_cursor()
        self.setup_draw_bindings()

    def set_tool_square(self):
        self.tool_settings.tool = "square"
        self.setup_cursor()
        self.setup_draw_bindings()

    def set_tool_triangle(self):
        self.tool_settings.tool = "triangle"
        self.setup_cursor()
        self.setup_draw_bindings()

    def set_tool_circle(self):
        self.tool_settings.tool = "circle"
        self.setup_cursor()
        self.setup_draw_bindings()

    def set_tool_eraser(self):
        self.tool_settings.tool = "eraser"
        self.setup_cursor()
        self.setup_draw_bindings()


    def change_size(self, event):
        tit = ""
        if self.tool_settings.tool == "pen":
            tit, s = "Pen", self.tool_settings.pen_size
        elif self.tool_settings.tool in ["square", "triangle", "circle"]:
            tit, s = "Figure", self.tool_settings.figure_size
        elif self.tool_settings.tool == "eraser":
            tit, s = "Eraser", self.tool_settings.eraser_size
        dialog = SizeDialog(self.root, tit, s)
        self.root.wait_window(dialog.dialog)
        if dialog.result is not None:
            if self.tool_settings.tool == "pen":
                self.tool_settings.pen_size = int(dialog.result["w"])
            elif self.tool_settings.tool in ["square", "triangle", "circle"]:
                self.tool_settings.figure_size = int(dialog.result["w"])
            elif self.tool_settings.tool == "eraser":
                self.tool_settings.eraser_size = int(dialog.result["w"])

    def change_color(self):
        color = colorchooser.askcolor(color=self.tool_settings.color)[1]
        if color != None:
            self.tool_settings.color = color
        else:
            return None
    def clear(self):
        self.current_tab.delete("all")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            self.current_tab.postscript(file="temp.ps", colormode="color")
            img = Image.open("temp.ps")
            img.save(file_path, format="png")
            img.close()
            os.remove("temp.ps")
            return True

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = Image.open(file_path)
            self.image = ImageTk.PhotoImage(image)
            if self.image_id:
                self.current_tab.delete(self.image_id)
            self.image_id = self.current_tab.create_image(0, 0, anchor=tk.NW, image=self.image)

    def is_cursor_inside(self, widget):
        cursor_x = widget.winfo_pointerx() - widget.winfo_rootx()
        cursor_y = widget.winfo_pointery() - widget.winfo_rooty()

        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()

        if 0 <= cursor_x < widget_width and 0 <= cursor_y < widget_height:
            return True
        else:
            return False


if __name__ == "__main__":
    window = MainWindow()
import  tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import *
from tkinter import messagebox
from PIL import ImageGrab

class SkecthPad:
    #Main
    def __init__(self) -> None:

        self.x = 0
        self.y = 0
        self.color = "black"                #start-up color
        self.root = tk.Tk()
        self.bg = "gray"
        self.root.title("Sketchpad")
        self.root.geometry("640x640")
        self.root.minsize(320, 320)

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Guardar", command=self.Guardar)
        self.filemenu.add_command(label="Info", command=self.info)

        self.menubar.add_cascade(menu=self.filemenu, label="Archivo")
        self.root.config(menu=self.menubar)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.frame = tk.Frame(self.root, bg="white")

        self.canvas = tk.Canvas(self.root ,bg=self.bg)

        self.slider = ttk.Scale(self.frame, orient="vertical", length=100, from_=50.0, to=1.0)
        self.btn1 = tk.Button(self.frame, text="Save", font="comicsans 12 bold")
        self.btn1.grid(column=0, row=1)
        self.btn2 = tk.Button(self.frame, text="Clear", font="comicsans 12 bold", command=self.Clear)
        self.btn2.grid(column=0, row=2)
        self.btn3 = tk.Button(self.frame, text="Color", font="comicsans 12 bold", command=self.ColorPick)
        self.btn3.grid(column=0, row=3)
        self.btn4 = tk.Button(self.frame, text="BG", font="comicsans 12 bold", command=self.ChangeBg)
        self.btn4.grid(column=0, row=4)
        
        self.status = tk.StringVar()
        self.status.set(f"x - 0 \ny - 0")

        self.statusbar = tk.Label(self.frame, textvariable=self.status, anchor="w", relief="sunken")
        self.statusbar.grid(column= 0, row= 5, sticky="s")

        self.slider.grid(column=0, row=0, sticky=("n"))
        self.canvas.grid(column=0, row=0, sticky=("NWES"))
        self.frame.grid(column=1, row=0, sticky=("nwe"))
        self.canvas.bind("<Motion>", self.captureMotion)
        self.canvas.bind("<Button-1>", self.RecordPos)
        self.canvas.bind("<Button-3>", self.RecordPos2)
        self.canvas.bind("<B1-Motion>", self.DrawLine) 
        self.canvas.bind("<B3-Motion>", self.DrawLine2)
        
        self.root.mainloop()

    #Functions
    def RecordPos(self, event):
        self.lastx, self.lasty = event.x, event.y

    def DrawLine(self, event):
        self.canvas.create_line((self.lastx, self.lasty, event.x, event.y), width=self.slider.get(), fill=self.color, smooth=True, capstyle="round")
        self.RecordPos(event)

    def RecordPos2(self, event):
        self.lastx, self.lasty = event.x, event.y

    def DrawLine2(self, event):
        self.canvas.create_line((self.lastx, self.lasty, event.x, event.y), width=self.slider.get(), fill=self.bg, smooth=True, capstyle="round", tags=('erase') )
        self.RecordPos2(event)

    def ColorPick(self):
        color = askcolor(color=self.color)[1]
        self.color = color

    def ChangeBg(self):
        color = askcolor(color=self.color)[1]
        self.bg = color
        self.canvas['bg'] = self.bg
        self.canvas.itemconfig('erase', fill=color)

    def Clear(self):
        global elem_info, canvas, created
        self.canvas.delete("all")
        elem_info = []
        created = []
        new = []

    def captureMotion(self, event):
        self.status.set(f"x - {event.x} \ny - {event.y}")
        self.statusbar.update()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Quiere Salir?"):
            self.root.destroy()

    def info(self):
        messagebox.showinfo(title="Info", message="Hecho por Federico Cando ;)")

    def Guardar(self):
        x=self.root.winfo_rootx()+self.canvas.winfo_x()
        y=self.root.winfo_rooty()+self.canvas.winfo_y()
        x1=x+self.canvas.winfo_width()
        y1=y+self.canvas.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("draw.jpg")

SkecthPad()



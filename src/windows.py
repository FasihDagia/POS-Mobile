from tkinter import ttk,messagebox,Frame
from src.database import database


class windows:
        
    def __init__(self,root):
        self.root = root
        self.db = database(self.root)
    
    def center_window(self,width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(width, height)

    def home_page(self):
        
        self.center_window(600,400)
        self.root.title("HomePage")

        buttons = ["Stock","Credit Accounts","Sales","Invoicing","Stock Entry"]

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),borderwidth=4,padding=(4,25))
        style.configure("Logout.TButton", font=("Helvetica", 11),borderwidth=4,padding=2)
        
        commmands = [self.stocks_window]

        btn_frame = Frame(self.root)
        btn_frame.pack(pady=10)
        
        row = 0
        col = 0
        counter = 0
        for button in buttons:            
            ttk.Button(btn_frame, text=button,style="Module.TButton" ,width=20, cursor="hand2",command=commmands[0]).grid(padx=10, pady=20, row=row,column=col)
            col+=1
            counter+=1
            if col == 3:
                row+=1
                col = 0

    def stocks_window(self):
        self.center_window(800,500)
        self.root.title("Stocks")

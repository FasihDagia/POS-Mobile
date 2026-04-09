from tkinter import ttk,messagebox,Frame,Toplevel,PhotoImage
from src.database import database
from src.utils import center_window,destroy_widgets,create_treeview


class windows:
        
    def __init__(self,root):
        self.root = root
        self.db = database(self.root)

    def landing_page(self):

        destroy_widgets(self.root)

        center_window(self.root,400,300)
        self.root.title("POS")

        ttk.Label(self.root,text="Point of Sale",font=("Helvetica",20,"bold")).pack(padx=50,pady=20)

        style = ttk.Style()
        style.configure("Log.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)
        style.configure("Log_exit.TButton", font=("Helvetica", 11),padding=3,borderwidth=2)

        ttk.Button(self.root,text="Login",style="Log.TButton",width=20, cursor="hand2",command=self.login).pack(padx=10, pady=15)
        ttk.Button(self.root,text="Exit",style="Log_exit.TButton",width=15,cursor="hand2", command=lambda:self.root.destroy()).pack(padx=10,pady=10)

    def login(self):
        
        popup = Toplevel(self.root)
        center_window(popup,400,225)
        popup.title("Custom Popup")

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(popup, image=smaller_img ,cursor="hand2",command=lambda:popup.destroy())
        bk_btn.image = smaller_img   
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(popup,text=f"Login",font=("Helvetica",20,"bold")).pack(padx=50,pady=10)
        ttk.Label(popup,text="Password")

        style = ttk.Style()
        style.configure("Login.TButton", font=("Helvetica", 11),borderwidth=4,padding=4)
        style.configure("Login_back.TButton", font=("Helvetica", 11),borderwidth=4,padding=2)

        entry_frame = Frame(popup)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame,text="Password:",font=("Helvetica",10)).grid(row=0,column=0,padx=10)
        password = ttk.Entry(entry_frame,width=30,show="*",font=("Helvetica",10,"bold"))
        password.grid(row=0,column=1,padx=10)

        login_button = ttk.Button(popup,text="Login",style="Login.TButton",width=20,cursor="hand2")
        login_button.pack(padx=10,pady=10)

        # bck_button = ttk.Button(btn_frame,text="Back",style="Login_back.TButton",width=15,cursor="hand2",command=login.destroy)
        # bck_button.grid(row=2,padx=10)


    def home_page(self):

        destroy_widgets(self.root)

        center_window(self.root, 600,400)
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
        destroy_widgets(self.root)

        center_window(self.root, 800,500)
        self.root.title("Stocks")

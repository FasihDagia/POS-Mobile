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

        def log():
            if self.db.get_password() is None:
                messagebox.showinfo("Setup", "No password found. Please create one.")
                self.create_password()
                return
            else:
                self.login()


        ttk.Button(self.root,text="Login",style="Log.TButton",width=20, cursor="hand2",command=log).pack(padx=10, pady=15)
        ttk.Button(self.root,text="Exit",style="Log_exit.TButton",width=15,cursor="hand2", command=lambda:self.root.destroy()).pack(padx=10,pady=10)

    def login(self):

        popup = Toplevel(self.root)
        center_window(popup, 400, 260)
        popup.title("Login")

        style = ttk.Style()
        style.configure("Log.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)
        style.configure("Log_exit.TButton", font=("Helvetica", 9),padding=3,borderwidth=2)


        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=lambda: popup.destroy())
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(popup, text="Login", font=("Helvetica", 20, "bold")).pack(pady=10)

        entry_frame = Frame(popup)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame, text="Password:", font=("Helvetica", 10)).grid(row=0, column=0, padx=10)

        password = ttk.Entry(entry_frame, width=30, show="*", font=("Helvetica", 10, "bold"))
        password.grid(row=0, column=1, padx=10)

        def handle_login():
            if self.db.verify_password(password.get()):
                messagebox.showinfo("Success", "Login Successful")
                self.home_page()   
                popup.destroy()
            else:
                messagebox.showerror("Error", "Incorrect Password")
                self.login()

        def forgot_password():
            popup.destroy()
            self.reset_password()

        ttk.Button(popup,text="Login",style="Log.TButton",width=20,cursor="hand2",command=handle_login).pack(pady=10)
        ttk.Button(popup,text="Forgot Password",style="Log_exit.TButton",cursor="hand2",command=forgot_password).pack()

    def create_password(self):
        popup = Toplevel(self.root)
        center_window(popup, 400, 235)
        popup.title("Set Password")

        style = ttk.Style()
        style.configure("Log_exit.TButton", font=("Helvetica", 10),padding=3,borderwidth=2)

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=lambda:popup.destroy())
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(popup, text="Create Password", font=("Helvetica", 18, "bold")).pack(pady=10)

        entry_frame = Frame(popup)
        entry_frame.pack()

        ttk.Label(entry_frame, text="Enter Password", font=("Helvetica", 10, "bold")).grid(row=0,column=0,pady=10)
        pw1 = ttk.Entry(entry_frame, show="*")
        pw1.grid(row=0,column=1, pady=5)

        ttk.Label(entry_frame, text="ReEnter Password", font=("Helvetica", 10, "bold")).grid(row=1,column=0,pady=10)
        pw2 = ttk.Entry(entry_frame, show="*")
        pw2.grid(row=1,column=1, pady=5)

        def save():
            if pw1.get() != pw2.get():
                messagebox.showerror("Error", "Passwords do not match")
                return

            if pw1.get() == "":
                messagebox.showerror("Error", "Password cannot be empty")
                return

            self.db.set_password(pw1.get())
            messagebox.showinfo("Success", "Password Created")
            self.login()
            popup.destroy()

        ttk.Button(popup, text="Save Password", style="Log_exit.TButton",cursor="hand2",width=15,command=save).pack(pady=10)

    def reset_password(self):
        popup = Toplevel(self.root)
        center_window(popup, 400, 235)
        popup.title("Reset Password")

        style = ttk.Style()
        style.configure("Log_exit.TButton", font=("Helvetica", 10),padding=3,borderwidth=2)

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(30, 30)

        def back():
            self.login()
            popup.destroy()

        bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=back)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(popup, text="Reset Password", font=("Helvetica", 18, "bold")).pack(pady=10)

        entry_frame = Frame(popup)
        entry_frame.pack()

        ttk.Label(entry_frame, text="Enter Password", font=("Helvetica", 10, "bold")).grid(row=0,column=0,pady=10)
        pw1 = ttk.Entry(entry_frame, show="*")
        pw1.grid(row=0,column=1, pady=5)

        ttk.Label(entry_frame, text="ReEnter Password", font=("Helvetica", 10, "bold")).grid(row=1,column=0,pady=10)
        pw2 = ttk.Entry(entry_frame, show="*")
        pw2.grid(row=1,column=1, pady=5)

        def update():
            if pw1.get() != pw2.get():
                messagebox.showerror("Error", "Passwords do not match")
                return

            if pw1.get() == "":
                messagebox.showerror("Error", "Password cannot be empty")
                return

            self.db.set_password(pw1.get())
            messagebox.showinfo("Success", "Password Updated")
            self.login()
            popup.destroy()

        ttk.Button(popup, text="Update Password", style="log_exit.TButton",cursor="hand2",command=update).pack(pady=10)            

    def home_page(self):

        destroy_widgets(self.root)

        center_window(self.root, 600,400)
        self.root.title("HomePage")

        img = PhotoImage(file="E:/POS Mobile/assets/logout.png")
        smaller_img = img.subsample(25, 25)

        bk_btn = ttk.Button(self.root,image=smaller_img,text="Logout",cursor="hand2",compound="left",style="Logout.TButton",command=self.landing_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="ne", padx=10, pady=10)


        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),borderwidth=4,padding=(4,25))
        style.configure("Logout.TButton", font=("Helvetica", 11),borderwidth=4,padding=2)
        
        buttons = ["Stock","Credit Accounts","Sales","Invoicing","Stock Entry"]
        commmands = [self.stocks_window]

        btn_frame = Frame(self.root)
        btn_frame.pack(pady=5)
        
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

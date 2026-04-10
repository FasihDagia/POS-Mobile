from tkinter import ttk,messagebox,Frame,Toplevel,PhotoImage,END,Canvas
from tkinter import *
from src.database import database
from src.utils import center_window,destroy_widgets,create_treeview,get_selected


class windows:
        
    def __init__(self,root):
        self.root = root
        self.db = database(self.root)
        self.imeis = []

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
        
        buttons = ["Stock","Stock Entry","Credit Accounts","Sales","Invoicing"]
        commmands = [self.stocks_window,self.stock_entry]

        btn_frame = Frame(self.root)
        btn_frame.pack(pady=5)
        
        row = 0
        col = 0
        counter = 0
        for button in buttons:            
            ttk.Button(btn_frame, text=button,style="Module.TButton" ,width=20, cursor="hand2",command=commmands[counter]).grid(padx=10, pady=20, row=row,column=col)
            col+=1
            counter+=1
            if col == 3:
                row+=1
                col = 0

    def stocks_window(self):
        destroy_widgets(self.root)

        center_window(self.root, 1000,600)
        self.root.title("Stocks")

        style = ttk.Style()
        style.configure("Log.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Remaining Stock",font=("Helvetica",20,"bold")).pack(pady=10)

        def show_imei():
            row = get_selected(table_stocks)
            if row:
                popup = Toplevel(self.root)
                popup.title("IMEI Nos")
                center_window(popup,350,550)

                img = PhotoImage(file="E:/POS Mobile/assets/back.png")
                smaller_img = img.subsample(30, 30)

                bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=lambda:popup.destroy())
                bk_btn.image = smaller_img
                bk_btn.pack(anchor="nw", padx=10, pady=10)

                model = row[2]
                ttk.Label(popup,text=f"Model:{model}",font=("Helvetica", 16, "bold")).pack(pady=7)
                table_imei_columns = ["S.NO","IMEI NO"]
                table_imei_width = [50,150]
                table_imei = create_treeview(popup,table_imei_columns,table_imei_width,20)
                self.db.load_imei(row,table_imei)        

            else:
                messagebox.showerror("Empty Input","Please Select a Mobile model")

        sh_btn = ttk.Button(self.root,text="Show IMEI",width=15,cursor="hand2",style="Log.TButton",command=show_imei)
        sh_btn.pack(pady=10)

        table_stock_columns =["S.NO", "Date Purchase","Model","Storage","Quantity", "Condition","Purchse Price","Selling Price"]
        table_stock_widths= [50,100,120,100,100,120,120,100,120] 
        table_stocks = create_treeview(self.root, table_stock_columns, table_stock_widths,20)
        self.db.load_stock(table_stocks)

    def stock_entry(self):

        destroy_widgets(self.root)
        center_window(self.root,600,450)

        self.root.title("Stock Entry")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(25, 25)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",style="Logout.TButton",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Stock Entry",font=("Helvetica",20,"bold")).pack(pady=5)

        font = ("Helvetica",10,"bold")
        entry_frame = Frame(self.root)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame,text="Date",font=font).grid(row=0,column=0,padx=5,pady=10)
        date_entry = ttk.Entry(entry_frame,font=font)
        date_entry.grid(row=0,column=1,padx=5,pady=10)

        ttk.Label(entry_frame,text="Model",font=font).grid(row=0,column=2,padx=5,pady=10)
        model_entry = ttk.Entry(entry_frame,font=font)
        model_entry.grid(row=0,column=3,padx=5,pady=10)

        ttk.Label(entry_frame,text="Storage",font=font).grid(row=1,column=0,padx=5,pady=10)
        storage_entry = ttk.Entry(entry_frame,font=font)
        storage_entry.grid(row=1,column=1,padx=5,pady=10)

        ttk.Label(entry_frame,text="Condition",font=font).grid(row=1,column=2,padx=5,pady=10)
        conditions = ["New","Used"]
        condition_entry = ttk.Combobox(entry_frame, values=conditions)
        condition_entry.grid(row=1,column=3,padx=5,pady=10)
        condition_entry.set("Select a condition")

        ttk.Label(entry_frame,text="Quantity",font=font).grid(row=2,column=0,padx=5,pady=10)
        quantity_entry = ttk.Entry(entry_frame,font=font)
        quantity_entry.grid(row=2,column=1,padx=5,pady=10)

        ttk.Label(entry_frame,text="Purchase Price",font=font).grid(row=2,column=2,padx=5,pady=10)
        purchase_price_entry = ttk.Entry(entry_frame,font=font)
        purchase_price_entry.grid(row=2,column=3,padx=5,pady=10)

        ttk.Label(entry_frame,text="Sell Price",font=font).grid(row=3,column=0,padx=5,pady=10)
        sell_price_entry = ttk.Entry(entry_frame,font=font)
        sell_price_entry.grid(row=3,column=1,padx=5,pady=10)

        ttk.Label(entry_frame,text="IMEI",font=font).grid(row=3,column=2,padx=5,pady=10)
        imei_button = ttk.Button(entry_frame,text="Enter IMEI Nos",cursor="hand2",command=lambda:imei_entry(quantity_entry))
        IMEI_entry = ttk.Entry(entry_frame,font=font)
        imei_button.grid(row=3,column=3,padx=5,pady=10)

        def imei_entry(quantity):
            quan = quantity.get()
            if quan:
                popup = Toplevel(self.root)
                popup.title("IMEI Entry")
                center_window(popup, 250, 350)
                ttk.Label(popup, text="IMEI Entry", font=("Helvetica", 12, "bold")).pack(pady=10)

                container = Frame(popup)
                container.pack(fill="both", expand=True)

                canvas = Canvas(container)
                scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

                scroll_frame = Frame(canvas)

                scroll_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )

                canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                def _on_mousewheel(event):
                    canvas.yview_scroll(-1 * (event.delta // 120), "units")

                canvas.bind_all("<MouseWheel>", _on_mousewheel)

                style = ttk.Style(scroll_frame)
                style.configure("Module.TButton",font=("Helvetica",9,"bold"))

                frame = Frame(scroll_frame)
                frame.pack(pady=5)

                for i in range(int(quan)):
                    ttk.Label(frame, text=f"IMEI {i+1}").grid(row=i,column=0, padx=5, pady=7)
                    ttk.Entry(frame, width=20).grid(row=i,column=1,pady=7)

                def get_imeis():
                    for entry in frame.winfo_children():
                        if not entry:
                            messagebox.showerror("Empty Input","Please Enter all Inputs")
                            break
                    for entry in frame.winfo_children():
                        if not isinstance(entry,ttk.Label):
                            self.imeis.append(entry.get())

                    popup.destroy()
                ttk.Button(scroll_frame,text="Submit",cursor="hand2",style="Module.TButton",command=get_imeis).pack(pady=5)

            else:
                messagebox.showerror("No Quantity","Plese Enter Quantity")

        ttk.Button(self.root,text="Add Stock",
                   cursor="hand2",style="Module.TButton",
                   command=lambda:self.db.add_stock(model_entry.get(),storage_entry.get(),
                                                    condition_entry.get(),date_entry.get(),
                                                    int(quantity_entry.get()),purchase_price_entry.get(),
                                                    sell_price_entry.get(),self.imeis)).pack(pady=10)


from tkinter import ttk,messagebox,Frame,Toplevel,PhotoImage,END,Canvas
from tkinter import *
from src.database import database
from src.utils import center_window,destroy_widgets,create_treeview,get_selected,grid_label,grid_create_treeview,print_invoice,clear_entries
from datetime import date,datetime


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
        ttk.Label(self.root,text="MH Point",font=("Helvetica",18,"bold")).pack(padx=50,pady=15)

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
        
        buttons = ["Stock","Stock Entry","Credit Accounts","Invoicing","Sales"]
        commmands = [self.stocks_window,self.stock_entry,self.credit_acc,self.invoicing,self.sales]

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

    def credit_acc(self):
        
        destroy_widgets(self.root)

        center_window(self.root,1100,600)
        self.root.title("Credit Accounts")
        
        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Credit Accounts",font=("Helvetica",20,"bold")).pack(pady=5)

        def show_history():
            row = get_selected(table_cr_acc)
            if row:
                popup = Toplevel(self.root)
                popup.title("Customer Account History")
                center_window(popup,800,600)

                img = PhotoImage(file="E:/POS Mobile/assets/back.png")
                smaller_img = img.subsample(30, 30)

                bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=lambda:popup.destroy())
                bk_btn.image = smaller_img
                bk_btn.pack(anchor="nw", padx=10, pady=10)

                ttk.Label(popup,text="Customer Account History",font=("Helvetica",17,"bold")).pack(pady=5)
                details_frame = Frame(popup)
                details_frame.pack(pady=10)

                ttk.Label(details_frame,text=f"Customer Name: {row[3]}",font=("Helvetica",12,"bold")).grid(row=0,column=0, padx=7, pady=5)
                ttk.Label(details_frame,text=f"Customer CNIC: {row[4]}",font=("Helvetica",12,"bold")).grid(row=0,column=1, padx=7, pady=5)
                ttk.Label(details_frame,text=f"Total Amount Paid: {row[6]}",font=("Helvetica",12,"bold")).grid(row=1,column=0, padx=7, pady=5)
                ttk.Label(details_frame,text=f"Balance: {row[7]}",font=("Helvetica",12,"bold")).grid(row=1,column=1, padx=7, pady=5)

                table_acc_his_columns =["S.NO", "Date","Amount Paid","Balance"]
                table_acc_his_widths= [50,100,130,120]
                table_acc_his = create_treeview(popup, table_acc_his_columns, table_acc_his_widths,18)
                self.db.load_cr_acc_history(row,table_acc_his)

            else:
                messagebox.showerror("Input Missing","Please Select a Customer!")
        
        btn_frame = Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame,text="Settel Account",style="Module.TButton",cursor="hand2",).grid(padx=7,pady=5,row=0,column=0)
        ttk.Button(btn_frame,text="Show History",style="Module.TButton",cursor="hand2",command=show_history).grid(padx=7,pady=5,row=0,column=1)

        table_cr_acc_columns =["S.NO", "Date","Next Due Date","Customer Name", "Customer CNIC","Down Payment","Total Amount Paid","Balance"]
        table_cr_acc_widths= [50,100,110,150,130,120,130,120]
        table_cr_acc = create_treeview(self.root, table_cr_acc_columns, table_cr_acc_widths,18)

        self.db.load_credit_acc(table_cr_acc)

    def invoicing(self):
        
        destroy_widgets(self.root)

        center_window(self.root, 1150,650)
        self.root.title("Invoiceing")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=4,borderwidth=2)
        style.configure("Save.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        entry_frame =Frame(self.root)
        entry_frame.pack(pady=15,padx=10)

        ttk.Label(entry_frame,text="Invoice",font=("Helvetica",20,"bold")).grid(row=0,column=0,columnspan=2,pady=7)
    
        right_frame = Frame(entry_frame)
        right_frame.grid(row=1,column=0,padx=10,sticky="ns")

        left_frame = Frame(entry_frame)
        left_frame.grid(row=1,column=1,padx=10,rowspan=2)

        grid_label(right_frame,"Date:",0,0,12)
        now = datetime.now()
        grid_label(right_frame,f"{now.strftime("%Y-%m-%d")}",1,0,12)

        grid_label(right_frame,"Invoice NO:",0,1,12)
        inv_no = f"INV{str(self.db.sales.count_documents({}) + 1).zfill(5)}"
        inv_no_label = ttk.Label(right_frame,text=inv_no,font=("Helvetica",12,"bold"))
        inv_no_label.grid(column=1,row=1,padx=5,pady=7)

        grid_label(right_frame,"Customer Name:",0,2,12)
        cus_name_entry = ttk.Entry(right_frame,font=("Helvetica",12,"bold"))
        cus_name_entry.grid(row=2,column=1,padx=5)

        grid_label(right_frame,"Customer CNIC:",0,3,12)
        cus_cnic_entry = ttk.Entry(right_frame,font=("Helvetica",12,"bold"))
        cus_cnic_entry.grid(row=3,column=1,padx=5)

        grid_label(right_frame,"Payment Type:",0,4,12)
        types = ["Paid in Full","Credit Sale"]
        pay_ty_entry = ttk.Combobox(right_frame, values=types)
        pay_ty_entry.grid(row=4,column=1,padx=5,pady=10)
        pay_ty_entry.set("Select type")

        dw_pay_label = ttk.Label(right_frame,text="Down Payment:",font=("Helvetica",12,"bold"),foreground="grey")
        dw_pay_entry = ttk.Entry(right_frame,font=("Helvetica",12,"bold"),state=["disabled"])

        dw_pay_label.grid(row=5,column=0,padx=5,pady=7)
        dw_pay_entry.grid(row=5,column=1,padx=5)

        def add_placeholder(entry, text):
            entry.delete(0, END)
            entry.insert(0, text)
            entry.configure(foreground="grey")

            def on_focus_in(event):
                if entry.get() == text:
                    entry.delete(0, END)
                    entry.configure(foreground="black")

            def on_focus_out(event):
                if entry.get() == "":
                    entry.delete(0, END)
                    entry.insert(0, text)
                    entry.configure(foreground="grey")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        nt_du_dt_label = ttk.Label(right_frame,text="Due Date:",font=("Helvetica",12,"bold"),foreground="grey")
        nt_du_dt_entry = ttk.Entry(right_frame,font=("Helvetica",12,"bold"),state=["disabled"])

        text = "(yyyy-mm-dd)"
        nt_du_dt_label.grid(row=6,column=0,padx=5,pady=7)
        nt_du_dt_entry.grid(row=6,column=1,padx=5)
        add_placeholder(nt_du_dt_entry,text)

        def cr_sale_input(event):
            type = pay_ty_entry.get()
            if type == "Credit Sale":
                dw_pay_label.configure(foreground="black")
                dw_pay_entry.configure(state=["!disabled"])

                nt_du_dt_label.configure(foreground="black")
                nt_du_dt_entry.configure(state=["!disabled"])
                add_placeholder(nt_du_dt_entry,text)
            else:
                dw_pay_label.configure(foreground="grey")
                dw_pay_entry.configure(state=["disabled"])

                nt_du_dt_label.configure(foreground="grey")
                nt_du_dt_entry.configure(state=["disabled"])
            
        pay_ty_entry.bind("<<ComboboxSelected>>", cr_sale_input)

        total_frame = Frame(entry_frame)
        total_frame.grid(pady=7,row=2,column=0)
        grid_label(total_frame,"Total",0,0,19)
        total_label = ttk.Label(total_frame,text=0.00,font=("Helvetica",19,"bold"))
        total_label.grid(row=0,column=1,pady=7)

        def total(pr):
            total = total_label.cget("text")
            total = total+float(pr)
            total_label.configure(text=total)

        ttk.Button(total_frame,text="Save",cursor="hand2",style="Save.TButton",command=lambda:save()).grid(row=1,column=0,columnspan=2,pady=7)

        def load_data():
            pipeline = [
                {
                    "$group": {
                        "_id": {
                            "model": "$model",
                            "storage": "$storage",
                            "condition": "$condition"
                        },
                        "imeis": {"$push": "$imei_nos"}
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "imeis": {
                            "$reduce": {
                                "input": "$imeis",
                                "initialValue": [],
                                "in": {
                                    "$concatArrays": ["$$value", "$$this"]
                                }
                            }
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "model": "$_id.model",
                            "storage": "$_id.storage"
                        },
                        "conditions": {
                            "$push": {
                                "condition": "$_id.condition",
                                "imeis": "$imeis"
                            }
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.model",
                        "storages": {
                            "$push": {
                                "storage": "$_id.storage",
                                "conditions": "$conditions"
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "model": "$_id",
                        "storages": 1
                    }
                }
            ]

            data = list(self.db.stock.aggregate(pipeline))
            return data

        data = load_data()

        model_data = {}
        for item in data:
            model_data[item["model"]] = {}

            for s in item["storages"]:
                storage_name = s["storage"]
                model_data[item["model"]][storage_name] = {}

                for c in s["conditions"]:
                    model_data[item["model"]][storage_name][c["condition"]] = c["imeis"]
                
        grid_label(left_frame,"Model:",0,0,11)
        model_entry = ttk.Combobox(left_frame)
        model_entry['values'] = list(model_data.keys())
        model_entry.grid(row=0,column=1,padx=5,pady=5)
        model_entry.set("Select  Model")

        grid_label(left_frame,"Storage:",2,0,11)
        storage_entry = ttk.Combobox(left_frame)
        storage_entry.grid(row=0,column=3,padx=5,pady=5)
        storage_entry.set("Select Storage")

        grid_label(left_frame,"Condition:",4,0,11)
        condition_entry = ttk.Combobox(left_frame)
        condition_entry.grid(row=0,column=5,padx=5,pady=5)
        condition_entry.set("Select Condition")

        grid_label(left_frame,"IMEI NO:",0,1,11)
        imei_entry = ttk.Combobox(left_frame)
        imei_entry.grid(row=1,column=1,padx=5,pady=7)
        imei_entry.set("Select IMEI NO")

        def on_model(event):
            m = model_entry.get()
            storage_entry['values'] = list(model_data[m].keys())

        def on_storage(event):
            m = model_entry.get()
            s = storage_entry.get()
            condition_entry['values'] = list(model_data[m][s].keys())

        def on_condition(event):
            m = model_entry.get()
            s = storage_entry.get()
            c = condition_entry.get()

            imeis = model_data[m][s][c]
            imei_entry['values'] = imeis

            filter = {
                "model": m,
                "storage":s,
                "condition":c
            }

            price = (self.db.stock.find_one(filter)).get("sell_price")
            total_label_in.configure(text=price)

        model_entry.bind("<<ComboboxSelected>>", on_model)
        storage_entry.bind("<<ComboboxSelected>>", on_storage)
        condition_entry.bind("<<ComboboxSelected>>", on_condition)

        grid_label(left_frame,"Price",2,1,11)
        total_label_in = ttk.Label(left_frame,text=0.00,font=("Helvetica",12,"bold"))
        total_label_in.grid(column=3,row=1,padx=5,pady=7)
        

        def add():
            model = model_entry.get()
            storage = storage_entry.get()
            condition = condition_entry.get()
            imei = imei_entry.get()
            if model == "Select Model" or storage == "Select Storage" or condition == "Select Condition" or imei == "Select IMEI NO":
                messagebox.showerror("Missing Fields","Please fill the missing feilds")
            else:
                filter = {
                    "model": model,
                    "storage":storage,
                    "condition":condition
                }
                price = (self.db.stock.find_one(filter)).get("sell_price")

                inv_table.insert("",END,values=(
                    len(inv_table.get_children())+1,
                    imei,
                    model,
                    storage,
                    condition,
                    price
                ))

                total(price)
                model_entry.set("Select Model")
                storage_entry.set("Select Storage")
                condition_entry.set("Select Condition")
                imei_entry.set("Select IMEI NO")
                
        ttk.Button(left_frame,text="Add",cursor="hand2",style="Module.TButton",command=add).grid(row=1,column=4,columnspan=2,padx=5)
        
        inv_table_columns = ["S.NO","IMEI NO","Model","Storage","Condition","Price"]
        inv_table_widths = [50,120,120,100,100,120]
        inv_table = grid_create_treeview(left_frame,inv_table_columns,inv_table_widths,18)

        def save():
            if not cus_name_entry.get() or not cus_cnic_entry.get() or pay_ty_entry.get() == "Select type":
                messagebox.showerror("Missing Feilds","Please fill all the fields")
                return
            if pay_ty_entry.get() == "Credit Sale":
                if not dw_pay_entry.get() or nt_du_dt_entry.get() == "(yyyy-mm-dd)":
                    messagebox.showerror("Missing Feilds","Please fill all the fields")
                    return
            
            data = []
            profit = 0
            balance = 0
            
            if pay_ty_entry.get() == "Credit Sale":
                dw_pay = dw_pay_entry.get()
                nt_du_dt = nt_du_dt_entry.get()
            else:
                dw_pay = 0
                nt_du_dt = "Nill"

            for entry in inv_table.get_children():
                values = inv_table.item(entry)["values"]

                row = {
                    "imei": str(values[1]),
                    "model": values[2],
                    "storage": values[3],
                    "condition": values[4],
                    "price": values[5]
                }
                data.append(row)

                    #profit calculator
                filter = {
                    "model":values[2],
                    "storage":values[3],
                    "condition":values[4]
                }
                stock_find = self.db.stock.find_one(filter)
                profit += (int(stock_find.get("sell_price"))-int(stock_find.get("purchase_price")))
                balance += (int(stock_find.get("sell_price"))-int(dw_pay))
                

            customer = {
                "name" : cus_name_entry.get(),
                "cnic": cus_cnic_entry.get(),
                "payment_type": pay_ty_entry.get(),
                "down_payment": dw_pay,
                "due_date": nt_du_dt,
                "balance": balance
            }

            
            now = datetime.now()
            invoice_info = {
                "invoice_no": inv_no_label.cget("text"),
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M"),
                "profit": profit,
                "total_inv_amount":int(total_label.cget("text"))
            }
            
            self.view_invoice(data,customer,invoice_info,inv_table,total_label,right_frame,inv_no_label,total_label_in)

    def view_invoice(self,data, customer, invoice_info,inv_table,total_label,frame,inv_no_label,total_label_in):

        win = Toplevel(self.root)
        win.title("Invoice Preview")
        win.geometry("600x700")
        win.configure(bg="white")

        img = PhotoImage(file="E:/POS Mobile/assets/back.png")
        smaller_img = img.subsample(35, 35)

        bk_btn = ttk.Button(win,image=smaller_img,cursor="hand2",command=lambda:win.destroy())
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        main = Frame(win, bg="white")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        ttk.Label(main, text="MH POINT", font=("Helvetica", 20, "bold"), background="white").pack()
        ttk.Label(main, text="The Name of Trust", font=("Helvetica", 14, "bold"), background="white").pack()

        ttk.Label(main,
            text="Shop # 42, Street # 11, Block-B, Baldia Complex, Mirpurkhas",background="white",font=("Helvetica",12)).pack()

        Label(main, text="Phone: 0336-0601994", background="white",font=("Helvetica",12)).pack()

        ttk.Separator(main).pack(fill="x", pady=10)

        info_frame = Frame(main, bg="white")
        info_frame.pack(fill="x")

        left = Frame(info_frame, bg="white")
        left.pack(side="left", fill="both", expand=True)

        right = Frame(info_frame, bg="white")
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(left, text=f"Customer: {customer['name']}", background="white",font=("Helvetica",10)).pack(anchor="center")
        ttk.Label(left, text=f"CNIC: {customer['cnic']}", background="white",font=("Helvetica",10)).pack(anchor="center")

        if customer["payment_type"].lower() == "credit sale":
            ttk.Label(left, text=f"Down Payment: {customer['down_payment']}", background="white",font=("Helvetica",10)).pack(anchor="center")
            ttk.Label(left, text=f"Due Date: {customer['due_date']}", background="white",font=("Helvetica",10)).pack(anchor="center")

        ttk.Label(right, text=f"Invoice No: {invoice_info['invoice_no']}", background="white",font=("Helvetica",10)).pack(anchor="center")
        ttk.Label(right, text=f"Date: {invoice_info['date']}", background="white",font=("Helvetica",10)).pack(anchor="center")
        ttk.Label(right, text=f"Time: {invoice_info['time']}", background="white",font=("Helvetica",10)).pack(anchor="center")
        ttk.Label(right, text=f"Payment: {customer['payment_type']}", background="white",font=("Helvetica",10)).pack(anchor="center")

        ttk.Separator(main).pack(fill="x", pady=10)

        table_frame = Frame(main, bg="white")
        table_frame.pack(fill="both", expand=True)

        tree_columns = ["S.No", "Description", "Amount"]
        tree_columns_width = [50,300,200]
        tree = create_treeview(table_frame,tree_columns,tree_columns_width,5)

        total = 0

        for i, item in enumerate(data, start=1):
            desc = f"{item['model']} {item['storage']} {item['condition']} (IMEI: {item['imei']})"
            amount = float(item["price"])

            total += amount
            tree.insert("", "end", values=(i, desc, amount))

        tree.insert("", "end", values=("", "TOTAL", total))

        tree.pack(fill="both", expand=True)

        ttk.Separator(main).pack(fill="x", pady=10)

        ttk.Label(main, text="Terms & Conditions", font=("Helvetica", 12, "bold"), background="white").pack(anchor="w")

        ttk.Label(main, text="• Goods once sold are not returnable.", background="white",font=("Helvetica",10)).pack(anchor="w")
        ttk.Label(main, text="• No warranty of panel on used phones", background="white",font=("Helvetica",10)).pack(anchor="w")
        ttk.Label(main, text="• 3 Days checking warranty on used phones", background="white",font=("Helvetica",10)).pack(anchor="w")
        ttk.Label(main, text="• The warranty on the box pack phones is provided by the company, The shop owner will not be responsible", background="white",font=("Helvetica",10)).pack(anchor="w")

        ttk.Label(main, text="Signature: ____________________", background="white").pack(pady=20, anchor="center")
        btn_frame = Frame(main)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Save",command=lambda: self.db.save_invoice(data,customer,invoice_info,frame,inv_table,total_label,win,inv_no_label,total_label_in)).grid(row=0,column=0,pady=10)
        ttk.Button(btn_frame, text="Save & Print",command=lambda:save_print).grid(row=0,column=1,pady=10)

        def save_print():
            self.db.save_invoice(data,customer,invoice_info,frame,inv_table,total_label,win,inv_no_label,total_label_in)
            print_invoice(data,customer,invoice_info)


    def sales(self):
        pass

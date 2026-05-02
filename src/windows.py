from tkinter import ttk,messagebox,Frame,Toplevel,PhotoImage,END,Canvas,BooleanVar,Checkbutton
from tkinter import *
from src.database import database
from src.utils import center_window,destroy_widgets,create_treeview,get_selected,grid_label,grid_create_treeview,print_invoice,add_placeholder,resource_path,remove_stock,validate_frame,stk_delete,stk_update
from src.utils import invoice_details
from datetime import date,datetime
from tkcalendar import DateEntry


class windows:
        
    def __init__(self,root):
        self.root = root
        self.db = database(self.root)
        self.imeis = {}
        self.timer = None

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
        popup.iconbitmap(resource_path("assets/point-of-sale.ico"))
        popup.title("Login")

        style = ttk.Style()
        style.configure("Log.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)
        style.configure("Log_exit.TButton", font=("Helvetica", 9),padding=3,borderwidth=2)


        img = PhotoImage(file=resource_path("assets/back.png"))
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
        password.focus_set()

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
        popup.iconbitmap(resource_path("assets/point-of-sale.ico"))
        popup.title("Set Password")

        style = ttk.Style()
        style.configure("Log_exit.TButton", font=("Helvetica", 10),padding=3,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
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
        pw1.focus_set()

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
        popup.iconbitmap(resource_path("assets/point-of-sale.ico"))
        popup.title("Reset Password")

        style = ttk.Style()
        style.configure("Log_exit.TButton", font=("Helvetica", 10),padding=3,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
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
        pw1.focus_set()

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

        img = PhotoImage(file=resource_path("assets/logout.png"))
        smaller_img = img.subsample(25, 25)

        bk_btn = ttk.Button(self.root,image=smaller_img,text="Logout",cursor="hand2",compound="left",style="Logout.TButton",command=self.landing_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="ne", padx=10, pady=10)


        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),borderwidth=4,padding=(4,25))
        style.configure("Logout.TButton", font=("Helvetica", 11),borderwidth=4,padding=2)
        
        buttons = ["Stock","Stock Entry","Credit Accounts","Invoicing Module","Sales"]
        commmands = [self.stocks_window,self.stock_entry,self.credit_acc,self.invoicing_module,self.sales]

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

    def invoicing_module(self):
        destroy_widgets(self.root)

        center_window(self.root, 600,300)
        self.root.title("Invoicing Module")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),borderwidth=4,padding=(4,25))

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Invoicing Module",font=("Helvetica",18,"bold")).pack(pady=10)

        btn_frame = Frame(self.root)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Generate Invoice",style="Module.TButton" ,width=20, cursor="hand2",command=self.invoicing).grid(padx=20, pady=20, row=0,column=0)
        ttk.Button(btn_frame, text="Return Invoice",style="Module.TButton" ,width=20, cursor="hand2",command=self.return_invoice).grid(padx=20, pady=20, row=0,column=1)

    def stocks_window(self):
        destroy_widgets(self.root)

        center_window(self.root, 1000,600)
        self.root.title("Stocks")

        style = ttk.Style()
        style.configure("Log.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Remaining Stock",font=("Helvetica",20,"bold")).pack(pady=10)

        def show_imei():
            row = get_selected(table_stocks)
            if row:
                filter1 = {"model":str(row[2])}
                is_mobile = self.db.stock.find_one(filter1)["is_mobile"]

                if is_mobile == True:
                    popup = Toplevel(self.root)
                    popup.title("IMEI Nos")
                    center_window(popup,400,550)

                    img = PhotoImage(file=resource_path("assets/back.png"))
                    smaller_img = img.subsample(30, 30)

                    def on_close():
                        self.db.load_stock(table_stocks)
                        popup.destroy()

                    bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=on_close)
                    bk_btn.image = smaller_img
                    bk_btn.pack(anchor="nw", padx=10, pady=10)

                    model = row[2]
                    ttk.Label(popup,text=f"Model:{model}",font=("Helvetica", 16, "bold")).pack(pady=7)
                    sup_entry_frame = Frame(popup)
                    sup_entry_frame.pack(pady=10)

                    grid_label(sup_entry_frame,"Supplier Name:",0,0,12)
                    suppliers = self.db.get_suppliers(row)
                    pay_ty_entry = ttk.Combobox(sup_entry_frame, values=suppliers)
                    pay_ty_entry.grid(row=0,column=1,padx=5,pady=10)
                    pay_ty_entry.set("Select a Supplier")

                    ttk.Button(sup_entry_frame,text="Show IMEI",cursor="hand2",command=lambda:self.db.load_imei(row,table_imei,pay_ty_entry)).grid(row=0,column=2,padx=5)

                    table_imei_columns = ["S.NO","IMEI NO"]
                    table_imei_width = [50,150]
                    table_imei = create_treeview(popup,table_imei_columns,table_imei_width,20)
                    
                    filter={
                        "model":str(row[2]),
                        "storage":str(row[3]),
                        "condition":str(row[5])
                    }

                    table_imei.bind("<Double-1>", lambda e: remove_stock(table_imei,pay_ty_entry.get(),self.db.stock,filter))
                    popup.protocol("WM_DELETE_WINDOW", on_close)

                else:
                    messagebox.showerror("Wrong Product","The product you have selected does not have IMEI Nos")
            else:
                messagebox.showerror("Empty Input","Please Select a Mobile model")

        def remove_stock_1():
            selected = table_stocks.selection()
            row = table_stocks.item(selected)["values"]
            filter1 = {"model":str(row[2])}
            is_mobile = self.db.stock.find_one(filter1)["is_mobile"]
            if is_mobile == False:
                
                dialog = Toplevel(self.root)
                dialog.title("Select Action")
                center_window(dialog,250,120)
                dialog.maxsize(250, 120)
                dialog.grab_set()  

                ttk.Label(dialog, text="What do you want to do?").pack(pady=10)

                ttk.Button(dialog, text="Delete", command=lambda:stk_delete(filter1,selected,dialog,self.db.stock,table_stocks)).pack(side="right", padx=10, pady=10)
                ttk.Button(dialog, text="Update", command=lambda:stk_update(filter1,selected,dialog,self.db.stock,table_stocks)).pack(side="right", padx=10, pady=10)

                
            else:
                messagebox.showerror("Can't Be Deleted","The product you have selected have IMEI Nos \nCan't be deleted from here")

        sh_btn = ttk.Button(self.root,text="Show IMEI",width=15,cursor="hand2",style="Log.TButton",command=show_imei)
        sh_btn.pack(pady=10)

        frame = Frame(self.root)
        frame.pack(pady=10)

        def search_data():
            query = search_entry.get().replace(" ","").lower()

            # Clear table
            table_stocks.delete(*table_stocks.get_children())
            all_data = self.db.stock.find()
            # Filter and insert only matching rows
            s_no = 1
            for item in all_data:
                if query in item["model"].replace(" ","").lower():
                    table_stocks.insert("", "end", values=(
                        s_no,
                        item["purchase_date"],
                        item["model"],
                        item.get("storage", ""),
                        item["quantity"],
                        item.get("condition", ""),
                        item["purchase_price"]
                    ))
                    s_no+=1

        search_entry = ttk.Entry(frame, width=30)
        search_entry.grid(row=0, column=0,sticky="w",padx=10)
        text ="Search"
        add_placeholder(search_entry,text)
        search_entry.bind("<KeyRelease>", lambda e: search_data())

        frame_2 = Frame(frame)
        frame_2.grid(row=1,column=0)
        table_stock_columns =["S.NO", "Date Purchase","Product","Storage","Quantity", "Condition","Purchse Price per Unit"]
        table_stock_widths= [50,100,120,100,100,120,120,200] 
        table_stocks = grid_create_treeview(frame_2, table_stock_columns, table_stock_widths,20)
        self.db.load_stock(table_stocks)

        table_stocks.bind("<Double-1>", lambda e: remove_stock_1())

    def stock_entry(self):

        destroy_widgets(self.root)
        center_window(self.root,600,450)

        self.root.title("Stock Entry")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(25, 25)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",style="Logout.TButton",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Stock Entry",font=("Helvetica",20,"bold")).pack(pady=5)

        font = ("Helvetica",10,"bold")
        entry_frame = Frame(self.root)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame,text="Date",font=font).grid(row=0,column=0,padx=5,pady=10)
        date_entry = DateEntry(entry_frame, width=12, background='darkblue',
                       foreground='white', borderwidth=2,date_pattern="yyyy-mm-dd")
        date_entry.grid(row=0,column=1,padx=5,pady=10)
        date_entry.set_date(date.today()) 

        ttk.Label(entry_frame,text="Product",font=font).grid(row=0,column=2,padx=5,pady=10)
        model_entry = ttk.Entry(entry_frame,font=font)
        model_entry.grid(row=0,column=3,padx=5,pady=10)

        ttk.Label(entry_frame,text="Supplier Name:",font=font).grid(row=1,column=0,padx=5,pady=10)
        supplier_name_entry = ttk.Entry(entry_frame,font=font)
        supplier_name_entry.grid(row=1,column=1,padx=5,pady=10)

        ttk.Label(entry_frame,text="Supplier CNIC:",font=font).grid(row=1,column=2,padx=5,pady=10)
        supplier_cnic_entry = ttk.Entry(entry_frame,font=font)
        supplier_cnic_entry.grid(row=1,column=3,padx=5,pady=10)
        
        ttk.Label(entry_frame,text="Quantity",font=font).grid(row=2,column=0,padx=5,pady=10)
        quantity_entry = ttk.Entry(entry_frame,font=font)
        quantity_entry.grid(row=2,column=1,padx=5,pady=10)
        
        ttk.Label(entry_frame,text="Purchase Price per Unit",font=font).grid(row=2,column=2,padx=5,pady=10)
        purchase_price_entry = ttk.Entry(entry_frame,font=font)
        purchase_price_entry.grid(row=2,column=3,padx=5,pady=10)
        
        def check_imei_enable():
            en_imei_entry = en_imei_entry_var.get()
            if en_imei_entry == True:
                imei_button.state(["!disabled"])
                storage_entry.state(["!disabled"])
                condition_entry.state(["!disabled"])
            else:
                imei_button.state(["disabled"])
                storage_entry.state(["disabled"])
                condition_entry.state(["disabled"])

        ttk.Label(entry_frame,text="Enable IMEI:",font=font).grid(row=3,column=0,padx=5,pady=10)
        en_imei_entry_var = BooleanVar(value=False)
        enable_imei_entry = Checkbutton(entry_frame,text="",variable=en_imei_entry_var,onvalue=True,offvalue=False,command=check_imei_enable)
        enable_imei_entry.grid(row=3, column=1, padx=5, pady=10)

        ttk.Label(entry_frame,text="Storage",font=font).grid(row=3,column=2,padx=5,pady=10)
        storage_entry = ttk.Entry(entry_frame,font=font,state=["disabled"])
        storage_entry.grid(row=3,column=3,padx=5,pady=10)

        ttk.Label(entry_frame,text="Condition",font=font).grid(row=4,column=0,padx=5,pady=10)
        conditions = ["New","Used"]
        condition_entry = ttk.Combobox(entry_frame, values=conditions,state=["disabled"])
        condition_entry.grid(row=4,column=1,padx=5,pady=10)
        condition_entry.set("Select a condition")

        ttk.Label(entry_frame,text="IMEI",font=font).grid(row=4,column=2,padx=5,pady=10)
        imei_button = ttk.Button(entry_frame,text="Enter IMEI Nos",cursor="hand2",command=lambda:imei_entry(quantity_entry,supplier_name_entry))
        imei_button.grid(row=4,column=3,padx=5,pady=10)
        imei_button.state(["disabled"])

        def imei_entry(quantity,supplier):
            quan = quantity.get()
            supplier_name = supplier.get()
            if quan and supplier_name: 
                popup = Toplevel(self.root)
                center_window(popup, 250, 350)
                popup.iconbitmap(resource_path("assets/point-of-sale.ico"))
                popup.title("IMEI Entry")
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
                    imei = []
                    for entry in frame.winfo_children():
                        if not entry:
                            messagebox.showerror("Empty Input","Please Enter all Inputs")
                            self.imeis.clear()
                            return
                    
                        elif not isinstance(entry,ttk.Label):
                                imei.append(entry.get())

                    self.imeis[supplier_name] = imei
                    

                    popup.destroy()
                ttk.Button(scroll_frame,text="Submit",cursor="hand2",style="Module.TButton",command=get_imeis).pack(pady=5)

            else:
                messagebox.showerror("No Quantity","Plese Enter Quantity")

        ttk.Button(self.root,text="Add Stock",cursor="hand2",style="Module.TButton",command=lambda:add_stock()).pack(pady=10)
        
        def reset_ui():
            for widget in entry_frame.winfo_children():
                if isinstance(widget, (Entry, ttk.Entry)):
                    widget.delete(0, 'end')

            date_entry.set_date(date.today()) 
            en_imei_entry_var.set(False)
            condition_entry.set("Select a condition")
            imei_button.state(["disabled"])
            storage_entry.state(["disabled"])
            condition_entry.state(["disabled"])

        def add_stock():
            date =  date_entry.get()
            product = model_entry.get()
            supplier_name = supplier_name_entry.get()
            supplier_cnic = supplier_cnic_entry.get()  
            quantity = int(quantity_entry.get())
            purchase_price = purchase_price_entry.get()
            is_mobile = en_imei_entry_var.get()
            if is_mobile == True:
                storage = storage_entry.get() 
                condition = condition_entry.get()
                imeis = self.imeis
            else:
                storage ="Nill"
                condition = "Nill"
                imeis = None

            validate = validate_frame(entry_frame)
            if validate == False or condition == "Select a condition":
                messagebox.showwarning("Missing Input","Please Fill all feilds")
                return
            else:   
                self.db.add_stock(product,storage,condition,date,quantity,purchase_price,imeis,supplier_name,supplier_cnic,is_mobile)
                reset_ui()

    def credit_acc(self):
        
        destroy_widgets(self.root)

        center_window(self.root,1100,600)
        self.root.title("Credit Accounts")
        
        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Credit Accounts",font=("Helvetica",20,"bold")).pack(pady=5)

        # def show_history():
        #     row = get_selected(table_cr_acc)
        #     if row:
        #         popup = Toplevel(self.root)
        #         popup.title("Customer Account History")
        #         center_window(popup,800,600)

        #         img = PhotoImage(file=resource_path("assets/back.png"))
        #         smaller_img = img.subsample(30, 30)

        #         bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=lambda:popup.destroy())
        #         bk_btn.image = smaller_img
        #         bk_btn.pack(anchor="nw", padx=10, pady=10)

        #         ttk.Label(popup,text="Customer Account History",font=("Helvetica",17,"bold")).pack(pady=5)
        #         details_frame = Frame(popup)
        #         details_frame.pack(pady=10)

        #         ttk.Label(details_frame,text=f"Customer Name: {row[3]}",font=("Helvetica",12,"bold")).grid(row=0,column=0, padx=7, pady=5)
        #         ttk.Label(details_frame,text=f"Customer CNIC: {row[4]}",font=("Helvetica",12,"bold")).grid(row=0,column=1, padx=7, pady=5)
        #         ttk.Label(details_frame,text=f"Total Amount Paid: {row[6]}",font=("Helvetica",12,"bold")).grid(row=1,column=0, padx=7, pady=5)
        #         ttk.Label(details_frame,text=f"Balance: {row[7]}",font=("Helvetica",12,"bold")).grid(row=1,column=1, padx=7, pady=5)

        #         table_acc_his_columns =["S.NO", "Date","Amount Paid","Balance"]
        #         table_acc_his_widths= [50,100,130,120]
        #         table_acc_his = create_treeview(popup, table_acc_his_columns, table_acc_his_widths,18)
        #         self.db.load_cr_acc_history(row,table_acc_his)

        #     else:
        #         messagebox.showerror("Input Missing","Please Select a Customer!")
        
        btn_frame = Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame,text="Settel Account",style="Module.TButton",cursor="hand2",command=lambda:self.settle_account(table_cr_acc)).grid(padx=7,pady=5,row=0,column=0)
        # ttk.Button(btn_frame,text="Show History",style="Module.TButton",cursor="hand2",command=show_history).grid(padx=7,pady=5,row=0,column=1)

        table_cr_acc_columns =["S.NO", "Last Payment Date","Next Due Date","Customer Name", "Customer CNIC","Down Payment","Total Amount Paid","Balance"]
        table_cr_acc_widths= [50,120,110,150,130,120,130,120]
        table_cr_acc = create_treeview(self.root, table_cr_acc_columns, table_cr_acc_widths,18)

        self.db.load_credit_acc(table_cr_acc)

    def settle_account(self,table):
        popup = Toplevel(self.root)
        center_window(popup,650,400)
        popup.title("Settle Credit Account")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(popup,image=smaller_img,cursor="hand2",command=lambda:popup.destroy())
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(popup,text="Settle Credit Account",font=("Helvetica",18,"bold")).pack(pady=15)
        
        entry_frame = Frame(popup)
        entry_frame.pack(pady=10)

        grid_label(entry_frame,"Date",0,0,11)
        date_entry = DateEntry(entry_frame, width=12, background='darkblue',
                       foreground='white', borderwidth=2,date_pattern="yyyy-mm-dd")
        date_entry.grid(row=0,column=1,padx=5,pady=10)
        date_entry.set_date(date.today()) 

        customer_names = []
        customer_cnics = []
        for customer in self.db.credit_accounts.find():
            customer_names.append(customer.get("customer_name"))
            customer_cnics.append(customer.get("customer_cnic"))

        grid_label(entry_frame,"Customer Name",2,0,11)
        customer_name_entry = ttk.Combobox(entry_frame, values=customer_names)
        customer_name_entry.grid(row=0,column=3,padx=5,pady=10)
        customer_name_entry.set("Select Name")

        grid_label(entry_frame,"Customer CNIC",0,1,11)
        customer_cnic_entry = ttk.Combobox(entry_frame, values=customer_cnics)
        customer_cnic_entry.grid(row=1,column=1,padx=5,pady=10)
        customer_cnic_entry.set("Select CNIC")
        
        grid_label(entry_frame,"Balance Amount:",2,1,11)
        bal_amount_label = ttk.Label(entry_frame,text=0.00,font=("Helvetica",12,"bold"))
        bal_amount_label.grid(column=3,row=1,padx=5,pady=7)

        def name_cnic_select(*args):
            if customer_name_entry.get() != "Select Name":
                cus =  self.db.credit_accounts.find_one({"customer_name":customer_name_entry.get()})
                customer_cnic_entry.set(cus.get("customer_cnic"))
                bal_amount_label.configure(text=cus.get("balance"))
            elif customer_cnic_entry.get()!="Select CNIC":
                cus =  self.db.credit_accounts.find_one({"customer_cnic":customer_cnic_entry.get()})
                customer_name_entry.set(cus.get("customer_name"))
                bal_amount_label.configure(text=cus.get("balance"))

        grid_label(entry_frame,"Amount Receivable:",0,2,11)
        amount_recev_entry = ttk.Entry(entry_frame,font=("Helvetica",11,"bold"))
        amount_recev_entry.grid(row=2,column=1,padx=5,pady=7)
        
        nt_du_dt_label = ttk.Label(entry_frame,text="Next Due Date:",font=("Helvetica",11,"bold"),foreground="grey")
        nt_du_dt_entry = ttk.Entry(entry_frame,font=("Helvetica",11,"bold"),state=["disabled"])

        text = "(yyyy-mm-dd)"
        nt_du_dt_label.grid(row=2,column=2,padx=5,pady=7)
        nt_du_dt_entry.grid(row=2,column=3,padx=5,pady=7)
        add_placeholder(nt_du_dt_entry,text)

        ttk.Label(entry_frame,text="Balance Due",font=("Helvetica",12,"bold")).grid(row=3,column=1,pady=10)
        bal_due_label = ttk.Label(entry_frame,text=0.00,font=("Helvetica",12,"bold"))
        bal_due_label.grid(row=3,column=2,pady=7)

        def on_change(event):
            
            if self.timer:
                self.root.after_cancel(self.timer)
            
            # set new timer (runs after 1 second of inactivity)
            self.timer = self.root.after(2000, amount_check)

        def amount_check(*args):
            amount = amount_recev_entry.get()
            if int(amount) > int(bal_amount_label.cget("text")):
                messagebox.showwarning("Amount Excess","Receivable Amount can't be greater than balance")
            elif int(amount) < int(bal_amount_label.cget("text")):
                nt_du_dt_label.configure(foreground="black")
                nt_du_dt_entry.configure(state=["!disabled"])
                add_placeholder(nt_du_dt_entry,text)
            else:
                nt_du_dt_label.configure(foreground="grey")
                nt_du_dt_entry.configure(state=["disabled"])
            
        def bal_due(*args):
            amount = amount_recev_entry.get()
            if amount:
                bal_due_label.configure(text=(int(bal_amount_label.cget("text"))-int(amount)))

        amount_recev_entry.bind("<KeyRelease>",on_change)
        amount_recev_entry.bind("<KeyRelease>",bal_due, add="+")

        customer_cnic_entry.bind("<<ComboboxSelected>>", name_cnic_select)
        customer_name_entry.bind("<<ComboboxSelected>>", name_cnic_select)

        ttk.Button(popup,text="Save",cursor="hand2",style="Module.TButton",command=lambda:save_cr()).pack(pady=15)

        def save_cr():
            data = {}

            try:
                
                date = date_entry.get()
                cus_name = customer_name_entry.get()
                cus_cnic = customer_cnic_entry.get()
                amount_receivable = amount_recev_entry.get()
                bal_due = int(bal_due_label.cget("text"))
                if bal_due > 0:
                    due_date = nt_du_dt_entry.get()
                else:
                    due_date = "Nill"
            except:
                messagebox.showerror("Missing Fields","Please Enter all fields")
            
            data["last_payment_dt"] = date
            data["customer_name"] = cus_name
            data["customer_cnic"] = cus_cnic
            data["amount_receivable"] = amount_receivable
            data["balance"] = bal_due
            data["due_date"] = due_date

            self.db.save_cr_settle(data)
            messagebox.showinfo("Account Updated","Credit account updated successfully!")
            popup.destroy()
            self.db.load_credit_acc(table)

    def invoicing(self):
        
        destroy_widgets(self.root)

        center_window(self.root, 1250,650)
        self.root.title("Generate Invoice")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=4,borderwidth=2)
        style.configure("Save.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.invoicing_module)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        entry_frame =Frame(self.root)
        entry_frame.pack(pady=15,padx=10)

        ttk.Label(entry_frame,text="Generate Invoice",font=("Helvetica",20,"bold")).grid(row=0,column=0,columnspan=2,pady=7)
    
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

        text = "Optional"
        grid_label(right_frame,"Customer Name:",0,2,12)
        cus_name_entry = ttk.Entry(right_frame,font=("Helvetica",12,"bold"))
        cus_name_entry.grid(row=2,column=1,padx=5)
        add_placeholder(cus_name_entry,text)

        grid_label(right_frame,"Customer CNIC:",0,3,12)
        cus_cnic_entry = ttk.Entry(right_frame,font=("Helvetica",12,"bold"))
        cus_cnic_entry.grid(row=3,column=1,padx=5)
        add_placeholder(cus_cnic_entry,text)

        grid_label(right_frame,"Payment Type:",0,4,12)
        types = ["Paid in Full","Credit Sale"]
        pay_ty_entry = ttk.Combobox(right_frame, values=types)
        pay_ty_entry.grid(row=4,column=1,padx=5,pady=10)
        pay_ty_entry.set("Select type")

        dw_pay_label = ttk.Label(right_frame,text="Down Payment:",font=("Helvetica",12,"bold"),foreground="grey")
        dw_pay_entry = ttk.Entry(right_frame,font=("Helvetica",12,"bold"),state=["disabled"])

        dw_pay_label.grid(row=5,column=0,padx=5,pady=7)
        dw_pay_entry.grid(row=5,column=1,padx=5)
        
        nt_du_dt_label = ttk.Label(right_frame,text="Due Date:",font=("Helvetica",12,"bold"),foreground="grey")
        nt_du_dt_entry = DateEntry(right_frame, width=12, background='darkblue',
                       foreground='white', borderwidth=2,date_pattern="yyyy-mm-dd",state=["disabled"])
        nt_du_dt_entry.set_date(date.today()) 

        nt_du_dt_label.grid(row=6,column=0,padx=5,pady=7)
        nt_du_dt_entry.grid(row=6,column=1,padx=5)

        grid_label(right_frame,"Note:",0,7,12)
        note_entry = Text(right_frame, height=5, width=30)
        note_entry.grid(row=7,column=1,padx=5,pady=10)

        def cr_sale_input(event):
            type = pay_ty_entry.get()
            if type == "Credit Sale":
                dw_pay_label.configure(foreground="black")
                dw_pay_entry.configure(state=["!disabled"])

                nt_du_dt_label.configure(foreground="black")
                nt_du_dt_entry.configure(state=["!disabled"])
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
                            "$addFields": {
                                "imei_nos": {
                                    "$reduce": {
                                        "input": {
                                            "$map": {
                                                "input": {"$objectToArray": "$imei_nos"},
                                                "as": "item",
                                                "in": "$$item.v"   # extract each supplier's array
                                            }
                                        },
                                        "initialValue": [],
                                        "in": {"$concatArrays": ["$$value", "$$this"]}
                                    }
                                }
                            }
                        },
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
                                        "in": {"$concatArrays": ["$$value", "$$this"]}
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
                
        def on_keyrelease(event):
            value = model_entry.get().lower()

            if value == "":
                data = all_models
            else:
                data = [item for item in all_models if value in item.lower()]

            model_entry['values'] = data

            # if data:
            #     model_entry.after(100, lambda: model_entry.event_generate('<Down>')) # open dropdown automatically

        grid_label(left_frame,"Product:",0,0,11)
        model_entry = ttk.Combobox(left_frame)
        model_entry['values'] = list(model_data.keys())
        model_entry.grid(row=0, column=1, padx=5, pady=5)
        model_entry.set("Select Model")

        all_models = list(model_data.keys())  # keep original list
        model_entry.bind("<KeyRelease>", on_keyrelease)

        grid_label(left_frame,"Storage:",2,0,11)
        storage_entry = ttk.Combobox(left_frame)
        storage_entry.grid(row=0,column=3,padx=5,pady=5)
        storage_entry.set("Select Storage")

        grid_label(left_frame,"Condition:",4,0,11)
        condition_entry = ttk.Combobox(left_frame)
        condition_entry.grid(row=0,column=5,padx=5,pady=5)
        condition_entry.set("Select Condition")

        second_row_frame = Frame(left_frame)
        second_row_frame.grid(row=1,column=0,columnspan=6)

        grid_label(second_row_frame,"IMEI NO:",0,0,11)
        imei_entry = ttk.Combobox(second_row_frame)
        imei_entry.grid(row=0,column=1,padx=5,pady=7)
        imei_entry.set("Select IMEI NO")

        grid_label(second_row_frame,"QTY:",2,0,11)
        qty_entry = ttk.Entry(second_row_frame,width=10,font=("Helvetica",11,"bold"))
        qty_entry.grid(row=0,column=3,padx=5,pady=7)

        def check_quantity(event):
            model = model_entry.get()
            if model != "Select Model":
                qty = int(qty_entry.get())
                find_qty =int(self.db.stock.find_one({"model":model}).get("quantity"))
                if qty > find_qty:
                    qty_entry.delete(0,'end')
                    qty_entry.insert(0,find_qty)
                    messagebox.showerror("Stock Unavailablity","Not enough stock is available in inventory.")
        
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

        def on_imei(event):
            imei = imei_entry.get()
            if imei != "Select IMEI NO":
                qty_entry.insert(0,"1")
                qty_entry.state(["disabled"])

        model_entry.bind("<<ComboboxSelected>>", on_model)
        storage_entry.bind("<<ComboboxSelected>>", on_storage)
        condition_entry.bind("<<ComboboxSelected>>", on_condition)
        imei_entry.bind("<<ComboboxSelected>>", on_imei)
        qty_entry.bind("<FocusOut>",check_quantity)

        grid_label(second_row_frame,"Price",4,0,11)
        total_entry_in = ttk.Entry(second_row_frame,font=("Helvetica",11,"bold"),width=15)
        total_entry_in.grid(column=5,row=0,padx=5,pady=7)
        

        def add():
            model = model_entry.get()
            storage = storage_entry.get()
            condition = condition_entry.get()
            imei = imei_entry.get()
            qty = int(qty_entry.get())
            price = int(total_entry_in.get())
            total_amount = qty*price

            filter4 = {"model":model} 
            if self.db.stock.find_one(filter4).get("is_mobile") == True:

                if model == "Select Model" or storage == "Select Storage" or condition == "Select Condition" or imei == "Select IMEI NO" or not price:
                    messagebox.showerror("Missing Fields","Please fill the missing feilds")
                    return
                else:

                    inv_table.insert("",END,values=(
                        len(inv_table.get_children())+1,
                        imei,
                        model,
                        storage,
                        condition,
                        qty,
                        price,
                        total_amount
                    ))
            else:
                if model == "Select Model" or not price:
                    messagebox.showerror("Missing Fields","Please fill the missing feilds")
                    return
                else:
                    inv_table.insert("",END,values=(
                        len(inv_table.get_children())+1,
                        "Nill",
                        model,
                        "Nill",
                        "Nill",
                        qty,
                        price,
                        total_amount
                    ))
            total(total_amount)
            model_entry.set("Select Model")
            storage_entry.set("Select Storage")
            condition_entry.set("Select Condition")
            imei_entry.set("Select IMEI NO")
            qty_entry.state(["!disabled"])
            qty_entry.delete(0,'end')
            total_entry_in.delete(0,'end')
                
        ttk.Button(second_row_frame,text="Add",cursor="hand2",style="Module.TButton",command=add).grid(row=0,column=6,padx=5)
        
        def remove_item():
            selected = inv_table.selection()

            if not selected:
                messagebox.showerror("No Selection", "Please select an item to remove")
                return

            for item in selected:
                values = inv_table.item(item, "values")
                price = float(values[5])  

                # subtract from total
                current_total = float(total_label.cget("text"))
                total_label.configure(text=current_total - price)

                inv_table.delete(item)

            for index, row in enumerate(inv_table.get_children(), start=1):
                values = list(inv_table.item(row, "values"))
                values[0] = index
                inv_table.item(row, values=values)
        
        table_frame = Frame(left_frame)
        table_frame.grid(row=2,column=0,columnspan=6)

        inv_table_columns = ["S.NO","IMEI NO","Product","Storage","Condition","QTY","Price","Total Amount"]
        inv_table_widths = [50,120,120,100,100,50,120,120]
        inv_table = grid_create_treeview(table_frame,inv_table_columns,inv_table_widths,18)

        inv_table.bind("<Double-1>", lambda e: remove_item())

        def reset_ui():
            for widget in right_frame.winfo_children():
                if isinstance(widget, (Entry, ttk.Entry)):
                    widget.delete(0, 'end')

            for row in inv_table.get_children():
                inv_table.delete(row)

            inv_no = f"INV{str(self.db.sales.count_documents({}) + 1).zfill(5)}"
            inv_no_label.configure(text=inv_no)

            total_label.configure(text=0.00)
            total_entry_in.delete(0,'end')

        def save():
            if pay_ty_entry.get() == "Select type":
                messagebox.showerror("Missing Feilds","Please fill all the fields")
                return
            if pay_ty_entry.get() == "Credit Sale":
                if not dw_pay_entry.get() or nt_du_dt_entry.get() == "(yyyy-mm-dd)" or cus_name_entry.get() =="Optional" or cus_cnic_entry.get() == "Optional":
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
            
            if cus_name_entry.get() =="Optional":
                customer_name = "Nill"
            else:
                customer_name = cus_name_entry.get()

            if cus_cnic_entry.get() =="Optional":
                customer_cnic = "Nill"
            else:
                customer_cnic = cus_cnic_entry.get()
            
            note = note_entry.get("1.0", END)

            if not note:
                note = "Nill"

            for entry in inv_table.get_children():
                
                values = inv_table.item(entry)["values"]
                filter = {
                    "model":str(values[2]),
                    "storage":str(values[3]),
                    "condition":str(values[4])
                }
                stock_find = self.db.stock.find_one(filter)
                supplier = None
                if stock_find.get("is_mobile") == True:
                    im = stock_find.get("imei_nos")
                    for key in im.keys():
                        for i in im[key]:
                            if i == str(values[1]):
                                supplier = key 

                row = {
                    "imei": str(values[1]),
                    "model": values[2],
                    "storage": values[3],
                    "condition": values[4],
                    "quantity": values[5],
                    "price": values[6],
                    "total_amount":values[7],
                    "is_mobile": stock_find.get("is_mobile"),
                    "supplier": supplier

                }
                data.append(row)

                profit += (int(values[5])-int(stock_find.get("purchase_price")))
                balance += (int(values[5])-int(dw_pay))
                

            customer = {
                "name" : customer_name,
                "cnic": customer_cnic,
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
                "total_inv_amount":int(total_label.cget("text")),
                "note":note
            }
            
            self.view_invoice(data, customer, invoice_info,"Generate", on_save=reset_ui)
        
    def view_invoice(self, data, customer, invoice_info,name, on_save=None):

        win = Toplevel(self.root)
        win.title("Invoice Preview")
        center_window(win, 600, 700)
        win.configure(bg="white")

        # --- Top Back Button ---
        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(35, 35)

        top_bar = Frame(win, bg="white")
        top_bar.pack(fill="x")

        bk_btn = ttk.Button(top_bar, image=smaller_img, cursor="hand2", command=win.destroy)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        # --- Scrollable Container ---
        container = Frame(win)
        container.pack(fill="both", expand=True,padx=8)

        canvas = Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both",expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Mouse Wheel Scroll ---
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        main = scrollable_frame

        # --- Header ---
        ttk.Label(main, text="MH POINT", font=("Helvetica", 20, "bold"), background="white").pack()
        ttk.Label(main, text="The Name of Trust", font=("Helvetica", 14, "bold"), background="white").pack()

        ttk.Label(
            main,
            text="Shop # 242, Street # 11, Block-B, Baldia Complex, Mirpurkhas",
            background="white"
        ).pack()

        ttk.Label(main, text="Phone: 0336-0601994", background="white").pack()

        ttk.Separator(main).pack(fill="x", pady=10)

        # --- Info Section ---
        info_frame = Frame(main, bg="white")
        info_frame.pack(fill="x")

        left = Frame(info_frame, bg="white")
        left.pack(side="left", fill="both", expand=True)

        right = Frame(info_frame, bg="white")
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(left, text=f"Customer: {customer['name']}", background="white").pack(anchor="center")
        ttk.Label(left, text=f"CNIC: {customer['cnic']}", background="white").pack(anchor="center")

        if customer["payment_type"].lower() == "credit sale":
            ttk.Label(left, text=f"Down Payment: {customer['down_payment']}", background="white").pack(anchor="center")
            ttk.Label(left, text=f"Due Date: {customer['due_date']}", background="white").pack(anchor="center")

        ttk.Label(right, text=f"Invoice No: {invoice_info['invoice_no']}", background="white").pack(anchor="center")
        ttk.Label(right, text=f"Date: {invoice_info['date']}", background="white").pack(anchor="center")
        ttk.Label(right, text=f"Time: {invoice_info['time']}", background="white").pack(anchor="center")
        ttk.Label(right, text=f"Payment: {customer['payment_type']}", background="white").pack(anchor="center")

        ttk.Separator(main).pack(fill="x", pady=10)

        # --- Table ---
        table_frame = Frame(main, bg="white")
        table_frame.pack(fill="both", expand=True)

        tree_columns = ["S.No", "Description", "Amount"]
        tree_columns_width = [50, 300, 200]
        tree = create_treeview(table_frame, tree_columns, tree_columns_width, 5)

        total = 0

        for i, item in enumerate(data, start=1):
            desc = item['model']

            if item.get("storage"):
                desc += f" {item['storage']}"
            if item.get("condition"):
                desc += f" {item['condition']}"
            if item.get("imei"):
                desc += f" (IMEI: {item['imei']})"

            amount = float(item["price"])
            total += amount

            tree.insert("", "end", values=(i, desc, amount))

        tree.insert("", "end", values=("", "TOTAL", total))

        if customer["payment_type"].lower() == "credit sale":
            down_payment = float(customer.get("down_payment", 0))
            balance = total - down_payment

            tree.insert("", "end", values=("", "Down Payment", down_payment))
            tree.insert("", "end", values=("", "Balance", balance))

        tree.pack(fill="both", expand=True)

        ttk.Separator(main).pack(fill="x", pady=10)

        # --- Note ---
        ttk.Label(main, text="Note", font=("Helvetica", 12, "bold"), background="white").pack(anchor="w")

        note_text = invoice_info.get("note", "").strip()
        note_text = note_text if note_text else "-"

        ttk.Label(
            main,
            text=note_text,
            background="white",
            wraplength=550,
            justify="left"
        ).pack(anchor="w", pady=5)

        ttk.Separator(main).pack(fill="x", pady=10)

        # --- Terms ---
        ttk.Label(main, text="Terms & Conditions", font=("Helvetica", 12, "bold"), background="white").pack(anchor="w")

        ttk.Label(main, text="• Goods once sold are not returnable.", background="white").pack(anchor="w")
        ttk.Label(main, text="• No warranty of panel on used phones", background="white").pack(anchor="w")
        ttk.Label(main, text="• 3 Days checking warranty on used phones", background="white").pack(anchor="w")
        ttk.Label(
            main,
            text="• The warranty on the box pack phones is provided by the company, The shop owner will not be responsible",
            background="white",
            wraplength=550,
            justify="left"
        ).pack(anchor="w")

        ttk.Label(main, text="Signature: ____________________", background="white").pack(pady=20)

        # --- Fixed Bottom Buttons ---
        btn_frame = Frame(win, bg="white")
        btn_frame.pack(fill="x", side="bottom", pady=10)

        def save_action():
            self.db.save_invoice(data, customer, invoice_info, win, on_save=on_save)

        def print_action():
            print_invoice(data, customer, invoice_info)

        def save_print():
            self.db.save_invoice(data, customer, invoice_info, win, on_save=on_save)
            print_invoice(data, customer, invoice_info)

        if name == "Generate":
            ttk.Button(btn_frame, text="Save", command=save_action).pack(side="left", expand=True, padx=10)
            ttk.Button(btn_frame, text="Print", command=print_action).pack(side="left", expand=True, padx=10)
            ttk.Button(btn_frame, text="Save & Print", command=save_print).pack(side="left", expand=True, padx=10)
        elif name == "view":
            ttk.Button(btn_frame, text="Print", command=print_action).pack(side="left", expand=True, padx=10)

    def sales(self):

        destroy_widgets(self.root)
        center_window(self.root,1100,600)

        self.root.title("Sales")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.home_page)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        ttk.Label(self.root,text="Sales",font=("Helvetica",20,"bold")).pack(pady=5)

        entry_frame = Frame(self.root)
        entry_frame.pack(pady=5)

        grid_label(entry_frame,"View From:",0,0,12)
        from_date = DateEntry(entry_frame, width=12, background='darkblue',
                       foreground='white', borderwidth=2,date_pattern="yyyy-mm-dd")
        from_date.grid(row=0,column=1,padx=5)

        grid_label(entry_frame,"View To:",2,0,12)
        to_date = DateEntry(entry_frame, width=12, background='darkblue',
                       foreground='white', borderwidth=2,date_pattern="yyyy-mm-dd")
        to_date.grid(row=0,column=3,padx=5)

        ttk.Button(entry_frame,text="view",cursor="hand2",command=lambda:view_info(from_date,to_date,no_inv_label,tot_sale_label,amt_recev_label)).grid(row=0,column=4,padx=5)

        info_entry = Frame(self.root)
        info_entry.pack(pady=5)

        grid_label(info_entry,"No Invoices:",0,0,11)
        no_inv_label = ttk.Label(info_entry,text=0,font=("helvetica",11,"bold"))
        no_inv_label.grid(padx=5,row=0,column=1)

        grid_label(info_entry,"Total Sale:",2,0,11)
        tot_sale_label = ttk.Label(info_entry,text=0,font=("helvetica",11,"bold"))
        tot_sale_label.grid(padx=5,row=0,column=3)

        grid_label(info_entry,"Amount Received:",4,0,11)
        amt_recev_label = ttk.Label(info_entry,text=0,font=("helvetica",11,"bold"))
        amt_recev_label.grid(padx=5,row=0,column=5)


        def view_inv():
            row = get_selected(table_sales)
            filter = {"invoice_no":row[2]}
            find = self.db.sales.find_one(filter)
            if find:
                data = []
                for prod in find.get("purchased_items"):
                    data.append({
                        "imei": prod.get("imei"),
                        "model": prod.get("model"),
                        "storage": prod.get("storage"),
                        "condition": prod.get("condition"),
                        "price": prod.get("price")
                    })
            
                invoice_info ={
                    "invoice_no":find.get("invoice_no"),
                    "date": find.get("inv_date"),
                    "time": find.get("inv_time"),
                    "total_inv_amount":find.get("total_inv_amount")
                }

                customer = {
                    "name" : find.get("customer_name"),
                    "cnic": find.get("customer_cnic"),
                    "payment_type": find.get("payment_type"),
                    "down_payment": find.get("down_payment"),
                    "due_date": find.get("due_date"),
                }

                self.view_invoice(data,customer,invoice_info,"view")
            else:
                messagebox.showerror("Invalid Invoice","Please Select a Invoice")

        ttk.Button(self.root,text="View Invoice",cursor="hand2",style="Module.TButton",command=view_inv).pack(pady=10)

        sales_table_columns = ["S NO","Date","Invoice NO","Customer Name","Customer CNIC","Payment Type","Total Invoice Amount","Amount Received"]
        sales_columns_width = [50,100,110,150,150,120,160,160]
        table_sales = create_treeview(self.root, sales_table_columns, sales_columns_width,18)
        self.db.load_sales(table_sales)

        def view_info(view_from,view_to,no_inv_label,tot_sale_label,amt_recev_label):
            from_date = view_from.get()
            to_date = view_to.get()

            if not from_date and not to_date:
                messagebox.showerror("Missing Fields","Both the Dates can't be empty!")
                return
            if len(table_sales.get_children()) == 0:
                messagebox.showerror("No Invoices","No Invoices generated")
                return

            if not from_date:
                from_date = self.db.sales.find_one({"invoice_no":"INV00001"}).get("inv_date")
            if not to_date:
                now = datetime.now()
                to_date = now.strftime("%Y-%m-%d")

            results = self.db.sales.find({
                "inv_date": {
                    "$gte": from_date,
                    "$lte": to_date
                }
            })
         
            if results:
                no_invoices = 0
                total_invoice_amount = 0.00
                amount_received = 0.00
                for result in results:
                    no_invoices+=1
                    total_invoice_amount += float(result.get("total_inv_amount"))
                    if float(result.get("down_payment")) == 0.00:
                        amount_received += float(result.get("total_inv_amount"))
                    else:
                        amount_received += float(result.get("down_payment"))
                if no_invoices == 0:
                    messagebox.showerror("No Invoices","No Invoices in the given date range!")
                    return
                else:
                    no_inv_label.config(text=no_invoices)
                    tot_sale_label.config(text=total_invoice_amount)
                    amt_recev_label.config(text=amount_received)

    def return_invoice(self):
        
        destroy_widgets(self.root)

        center_window(self.root, 1170,650)
        self.root.title("Return Invoice")

        style = ttk.Style()
        style.configure("Module.TButton", font=("Helvetica", 11),padding=4,borderwidth=2)
        style.configure("Save.TButton", font=("Helvetica", 11),padding=6,borderwidth=2)

        img = PhotoImage(file=resource_path("assets/back.png"))
        smaller_img = img.subsample(30, 30)

        bk_btn = ttk.Button(self.root,image=smaller_img,cursor="hand2",command=self.invoicing_module)
        bk_btn.image = smaller_img
        bk_btn.pack(anchor="nw", padx=10, pady=10)

        entry_frame =Frame(self.root)
        entry_frame.pack(pady=15,padx=10)

        ttk.Label(entry_frame,text="Return Invoice",font=("Helvetica",20,"bold")).grid(row=0,column=0,columnspan=2,pady=7)
    
        right_frame = Frame(entry_frame)
        right_frame.grid(row=1,column=0,padx=10,sticky="ns")

        left_frame = Frame(entry_frame)
        left_frame.grid(row=1,column=1,padx=10,rowspan=2)

        grid_label(right_frame,"Date:",0,0,12)
        date_label = ttk.Label(right_frame,text="-",font=("Helvetica",12,"bold"))
        date_label.grid(row=0,column=1,padx=5)

        grid_label(right_frame,"Invoice NO:",0,1,12)
        invoices = []
        for inv in self.db.sales.find():
            if inv.get("returned") == False:
                invoices.append(inv.get("invoice_no"))
        inv_entry = ttk.Combobox(right_frame, values=invoices)
        inv_entry.grid(column=1,row=1,padx=5,pady=7)
        inv_entry.set("Select Invoice")
        
        
        grid_label(right_frame,"Customer Name:",0,2,12)
        cus_name_entry = ttk.Label(right_frame,text="-",font=("Helvetica",12,"bold"))
        cus_name_entry.grid(row=2,column=1,padx=5)
        
        grid_label(right_frame,"Customer CNIC:",0,3,12)
        cus_cnic_entry = ttk.Label(right_frame,text="-",font=("Helvetica",12,"bold"))
        cus_cnic_entry.grid(row=3,column=1,padx=5)
        
        grid_label(right_frame,"Payment Type:",0,4,12)
        pay_ty_entry =  ttk.Label(right_frame,text="-",font=("Helvetica",12,"bold"))
        pay_ty_entry.grid(row=4,column=1,padx=5,pady=10)

        dw_pay_label = ttk.Label(right_frame,text="Down Payment:",font=("Helvetica",12,"bold"))
        dw_pay_entry =  ttk.Label(right_frame,text="-",font=("Helvetica",12,"bold"))

        dw_pay_label.grid(row=5,column=0,padx=5,pady=7)
        dw_pay_entry.grid(row=5,column=1,padx=5)
        
        nt_du_dt_label = ttk.Label(right_frame,text="Due Date:",font=("Helvetica",12,"bold"))
        nt_du_dt_entry =  ttk.Label(right_frame,text="-",font=("Helvetica",12,"bold"))

        nt_du_dt_label.grid(row=6,column=0,padx=5,pady=7)
        nt_du_dt_entry.grid(row=6,column=1,padx=5)

        grid_label(right_frame,"Note:",0,7,12)
        note_entry = ttk.Label(right_frame,text="-",font=("Helvetica",12,"bold"))
        note_entry.grid(row=7,column=1,padx=5,pady=12)

        inv_table_columns = ["S.NO","IMEI NO","Product","Storage","Condition","Price"]
        inv_table_widths = [50,120,120,100,100,120]
        inv_table = grid_create_treeview(left_frame,inv_table_columns,inv_table_widths,18)

        total_frame = Frame(entry_frame)
        total_frame.grid(pady=7,row=2,column=0)
        grid_label(total_frame,"Total",0,0,19)
        total_label = ttk.Label(total_frame,text=0.00,font=("Helvetica",19,"bold"))
        total_label.grid(row=0,column=1,pady=7)

        ttk.Button(total_frame,text="Return",cursor="hand2",style="Save.TButton",command=lambda:retur(inv_table)).grid(row=1,column=0,columnspan=2,pady=7)

        labels ={
            "date":date_label,
            "customer_name":cus_name_entry,
            "customer_cnic":cus_cnic_entry,
            "payment_type":pay_ty_entry,
            "down_payment":dw_pay_entry,
            "next_due_date":nt_du_dt_entry,
            "note":note_entry,
            "total_invoice_amount":total_label
        }

        inv_entry.bind("<<ComboboxSelected>>", lambda e: invoice_details(inv_entry.get(),self.db.sales,labels,inv_table))

        def retur(table):
            invoice_no = inv_entry.get()
            selected = get_selected(table)
            if invoice_no == "Select Invoice" or  invoice_no.replace(" ","") == "":
                messagebox.showwarning("Invoice Missing","No Invoice selected")
                return
            filter = {"invoice_no":invoice_no}
            find = self.db.sales.find_one(filter)
            if not find:
                messagebox.showwarning("Invalid Invoice","Please select a valid invoice number!")
                return
            total_rows = len(table.get_children())
            if total_rows == 1:
                confirm = messagebox.askyesno("Confirm","Are you sure you wnat to Return the Invoice?")
                if confirm:
                    pass
            elif total_rows > 1:
                if not selected:
                    confirm =  messagebox.askyesno("Confirm","Are you sure you wnat to Return the entire Invoice?")
                    if confirm:
                        pass
                elif selected:
                    confirm =  messagebox.askyesno("Confirm","Are you sure you wnat to Return the Product?")
                    if confirm:
                        pass


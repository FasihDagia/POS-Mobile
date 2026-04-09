def login(self):

    popup = Toplevel(self.root)
    center_window(popup, 400, 260)
    popup.title("Login")

    # BACK BUTTON
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

    # ================= LOGIN FUNCTION =================
    def handle_login():
        if self.db.get_password() is None:
            messagebox.showinfo("Setup", "No password found. Please create one.")
            popup.destroy()
            self.create_password()
            return

        if self.db.verify_password(password.get()):
            messagebox.showinfo("Success", "Login Successful")
            popup.destroy()
            self.home_page()   # or your main system page
        else:
            messagebox.showerror("Error", "Incorrect Password")

    # ================= FORGOT PASSWORD =================
    def forgot_password():
        popup.destroy()
        self.reset_password()

    ttk.Button(popup,text="Login",style="Login.TButton",width=20,cursor="hand2",command=handle_login).pack(pady=10)
    ttk.Button(popup,text="Forgot Password",cursor="hand2",command=forgot_password).pack()
import sys
import os
from tkinter import messagebox,END
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import hashlib
from dotenv import load_dotenv

class database:
    def __init__(self,root):
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        try:
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000
            )
            self.client.server_info()

        except PyMongoError as e:

            root.withdraw()
            messagebox.showerror(
                "Database Connection Error",
                f"Failed to connect to database\n Contact Developer"
            )
            root.destroy()
            sys.exit()
            
        self.db = self.client["mobile_shop"]
        self.stock = self.db["stock"]
        self.credit_accounts= self.db["credit_accounts"]
        self.credit_accounts_history = self.db["credit_accounts_history"]
        self.sales = self.db["sales"]
        self.auth = self.db["auth"]
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_password(self):
        data = self.auth.find_one({"type": "password"})
        return data["value"] if data else None

    def set_password(self, password):
        hashed = self.hash_password(password)

        self.auth.update_one(
            {"type": "password"},
            {"$set": {"value": hashed}},
            upsert=True
        )

    def verify_password(self, password):
        stored = self.get_password()
        return stored == self.hash_password(password)

    def add_stock(self, model, storage, condition, purchase_date, quantity, purchase_price,sell_price,imei_nos):

        data = {
            "purchase_date": purchase_date,
            "model": model,
            "storage": storage,
            "condition": condition,
            "quantity": quantity,
            "purchase_price": purchase_price,
            "sell_price": sell_price,
            "imei_nos":imei_nos
        }

        filter = {
            "model": model,
            "storage": storage,
            "condition": condition,
        }
        exist = self.stock.find_one(filter)
        
        if exist:
            imei = exist.get("imei_nos")
            quantity = quantity+ exist["quantity"]
            for imeis in imei_nos:
                imei.append(imeis)
            data["imei_nos"] = imei
            data["quantity"] = quantity

            self.stock.update_one(filter,{"$set":data})
        else:
            self.stock.insert_one(data)

        imei_nos.clear()

        messagebox.showinfo("Success","Stock added successfully!")
    
    def load_stock(self,table):

        for row in table.get_children():
            table.delete(row)

        entries = self.stock.find()

        s_no =1
        for entry in entries:
            table.insert("", END,values=(
                s_no,
                entry.get("purchase_date"),
                entry.get("model"),
                entry.get("storage"),
                entry.get("quantity"),
                entry.get("condition"),
                entry.get("purchase_price"),
                entry.get("sell_price"),
            ))
            s_no+=1

    def load_imei(self,row,table):
        
        for ro in table.get_children():
            table.delete(ro)

        filter = {
            "model":row[2],
            "storage":row[3],
            "condition":row[5]
        }

        data = self.stock.find_one(filter)
        imeis = data.get("imei_nos")
        s_no =1
        for entry in imeis:
            table.insert("", END,values=(
                s_no,
                entry
                ))
            
    def load_cr_acc_history(self,row,table):
        
        for ro in table.get_children():
            table.delete(ro)

        filter ={
            "customer_name":row[4],
            "customer_cnic":row[5]
        }

        history = self.credit_accounts_history.find(filter)
        s_no = 1
        for entry in history:
            table.insert("",END,values=(
                s_no,
                entry.get("date"),
                entry.get("amount_paid"),
                entry.get("balance")
            )) 
            s_no+=1

    def save_invoice(self,):
        pass
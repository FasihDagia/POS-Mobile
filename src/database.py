import sys
import os
from tkinter import messagebox
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


        messagebox.showinfo("Success","Stock added successfully!")
    
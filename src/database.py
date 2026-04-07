import sys
import os
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.errors import PyMongoError
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
    
    def add_stock(self, model, brand, storage, ram, battery, camera, condition, specs, purchase_date, quantity, purchase_price,sell_price,imei_nos):
        data = {
            "model": model,
            "brand": brand,
            "storage": storage,
            "ram": ram,
            "battery": battery,
            "camera": camera,
            "condition": condition,
            "specs": specs,
            "purchase_date": purchase_date,
            "sell_date": "",
            "quantity": quantity,
            "purchase_price": purchase_price,
            "sell_price": sell_price,
            "imei_nos":imei_nos
        }

        self.stock.insert_one(data)

    
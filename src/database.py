import sys
import os
from tkinter import messagebox,END
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import hashlib
from tkinter import ttk
from tkinter import *
from src.utils import env_resource_path
from dotenv import load_dotenv
import certifi

class database:
    def __init__(self,root):
        load_dotenv(env_resource_path(".env"))
        mongo_uri = os.getenv("MONGO_URI")
        try:
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,
                tls=True,
                tlsCAFile=certifi.where() 
            )
            self.client.server_info()

        except PyMongoError as e:

            root.withdraw()
            messagebox.showerror(
                "Database Connection Error",
                f"Failed to connect to database\n Contact Developer\n{e}"
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
            
    def save_invoice(self,data,customer,invoice_info,win,on_save=None):

        details = {
            "invoice_no":invoice_info["invoice_no"],
            "inv_date": invoice_info["date"],
            "inv_time":invoice_info["time"],
            "customer_name":customer["name"],
            "customer_cnic":customer["cnic"],
            "payment_type": customer["payment_type"],
            "down_payment":customer["down_payment"],
            "due_date": customer["due_date"],
            "purchased_items": data,
            "total_inv_amount":invoice_info["total_inv_amount"],
            "profit":invoice_info["profit"]

        }

        details_cr = {
            "invoice_no":invoice_info["invoice_no"],
            "inv_date": invoice_info["date"],
            "inv_time":invoice_info["time"],
            "customer_name":customer["name"],
            "customer_cnic":customer["cnic"],
            "payment_type": customer["payment_type"],
            "down_payment":customer["down_payment"],
            "due_date": customer["due_date"],
            "purchased_items": data,
            "total_amount_paid":customer["down_payment"],
            "balance": customer["balance"],
            "status":"unsettled"
        }

        for items in data:
            filter1 ={
                "model":items["model"],
                "storage":items["storage"],
                "condition":items["condition"]
            }
            stck_find = self.stock.find_one(filter1)
            quan = stck_find.get("quantity") - 1
            imeis = stck_find.get("imei_nos")
            imeis.remove(items["imei"])
            if quan == 0:
                self.stock.delete_one(filter1)
            else:
                self.stock.update_one(filter1,{"$set":{"quantity":quan,"imei_nos":imeis}})

        self.sales.insert_one(details)

        if customer["payment_type"] == "Credit Sale":
            self.credit_accounts_history.insert_one(details_cr)

            filter = {
                "customer_name":customer["name"],
                "customer_cnic":customer["cnic"]
            }

            acc_find = self.credit_accounts.find_one(filter)
            if acc_find:
                self.credit_accounts.update_one(filter,{"$set":{"down_payment":int(acc_find["down_payment"])+int(customer["down_payment"]),
                                                                  "total_amount_paid":int(acc_find["total_amount_paid"])+int(customer["down_payment"]),
                                                                  "balance":int(acc_find["balance"])+customer["balance"],
                                                                  "due_date":customer["due_date"]}})
            else:
                self.credit_accounts.insert_one(details_cr) 

            
        
        messagebox.showinfo("Success","Invoice Saved successfuly!")
        if on_save:
            on_save()
        win.destroy()

    def load_credit_acc(self,table):
        
        for row in table.get_children():
            table.delete(row)

        entries = self.credit_accounts.find()

        s_no =1
        for entry in entries:
            if entry.get("status") == "unsettled":
                table.insert("", END,values=(
                    s_no,
                    entry.get("inv_date"),
                    entry.get("due_date"),
                    entry.get("customer_name"),
                    entry.get("customer_cnic"),
                    entry.get("down_payment"),
                    entry.get("total_amount_paid"),
                    entry.get("balance"),
                ))
                s_no+=1

    def save_cr_settle(self,data):
        filter = {
            "customer_name": data["customer_name"],
            "customer_cnic":data["customer_cnic"]
        }
        entry = self.credit_accounts.find_one(filter)
        if entry:
            if data["balance"] == 0:
                self.credit_accounts.update_one(entry,{"$set":{
                    "inv_date": data["last_payment_dt"],
                    "due_date":data["due_date"],
                    "total_amount_paid": (int(entry.get("total_amount_paid"))+int(data["amount_receivable"])),
                    "balance": data["balance"],
                    "status":"settled"
                }})
            else:
                self.credit_accounts.update_one(entry,{"$set":{
                    "inv_date": data["last_payment_dt"],
                    "due_date":data["due_date"],
                    "total_amount_paid": (int(entry.get("total_amount_paid"))+int(data["amount_receivable"])),
                    "balance": data["balance"],
                }})
            self.credit_accounts_history.insert_one(data)

    def load_sales(self,table):
        for row in table.get_children():
            table.delete(row)

        entries = self.sales.find()
        s_no =1
        for entry in entries:
            if entry.get("down_payment") == 0:
                table.insert("", END,values=(
                    s_no,
                    entry.get("inv_date"),
                    entry.get("invoice_no"),
                    entry.get("customer_name"),
                    entry.get("customer_cnic"),
                    entry.get("payment_type"),
                    entry.get("total_inv_amount"),
                    entry.get("total_inv_amount"),
                ))
            else:
                table.insert("", END,values=(
                    s_no,
                    entry.get("inv_date"),
                    entry.get("invoice_no"),
                    entry.get("customer_name"),
                    entry.get("customer_cnic"),
                    entry.get("payment_type"),
                    entry.get("total_inv_amount"),
                    entry.get("down_payment"),
                ))
            s_no+=1

    # def load_cr_acc_history(self,row,table):
        
    #     for ro in table.get_children():
    #         table.delete(ro)

    #     filter ={
    #         "customer_name":row[3],
    #         "customer_cnic":row[4]
    #     }

    #     history = self.credit_accounts_history.find(filter)
    #     s_no = 1
    #     for entry in history:
    #         table.insert("",END,values=(
    #             s_no,
    #             entry.get("inv_date"),
    #             entry.get("down_payment"),
    #             entry.get("balance")
    #         )) 
    #         s_no+=1
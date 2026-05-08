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
            
        self.db = self.client["test"]
        self.stock = self.db["stock"]
        self.credit_accounts= self.db["credit_accounts"]
        self.sales = self.db["sales"]
        self.auth = self.db["auth"]
        self.ledger = self.db["ledger"]
        self.returned_invoices = self.db["returned_invoices"]
    
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

    def add_stock(self, model, storage, condition, purchase_date, quantity, purchase_price,imei_nos,supplier_name,supplier_cnic,is_mobile):

            data = {
                "purchase_date": purchase_date,
                "model": model,
                "is_mobile":is_mobile,
                "storage": storage,
                "condition": condition,
                "quantity": quantity,
                "purchase_price": purchase_price,
                "imei_nos":imei_nos,
                "suppliers":{
                    "1":{
                    "name":supplier_name,
                    "cnic":supplier_cnic
                }}
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
                suppliers = exist.get("suppliers")
                if imei:
                    if supplier_name in imei.keys():
                        sup_imeis = imei[supplier_name]
                        for imeis in imei_nos[supplier_name]:
                            sup_imeis.append(imeis)
                        imei[supplier_name] = sup_imeis
                    else:
                        imei[supplier_name] = imei_nos[supplier_name]  
                new_supplier = data["suppliers"]["1"]
                exists = any(s["cnic"] == new_supplier["cnic"] for s in suppliers.values())

                if not exists:
                    new_id = str(len(suppliers.keys())+1)
                    suppliers[new_id] = new_supplier
                
                data["imei_nos"] = imei
                data["quantity"] = quantity
                data["suppliers"] = suppliers

                self.stock.update_one(filter,{"$set":data})
            else:
                self.stock.insert_one(data)
            if imei_nos:
                imei_nos.clear()

            messagebox.showinfo("Success","Stock added successfully!")
    
    def load_stock(self,table):

        for row in table.get_children():
            table.delete(row)

        entries = self.stock.find()

        s_no =1
        for entry in entries:
            if entry.get("quantity") > 0:
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

    def load_imei(self,row,table,supplier):
        suply = supplier.get()
        if suply:
            for ro in table.get_children():
                table.delete(ro)

            filter = {
                "model":str(row[2]),
                "storage":str(row[3]),
                "condition":str(row[5])
            }

            data = self.stock.find_one(filter)
            imeis = data.get("imei_nos")
            suply_imei = imeis[suply]
            s_no =1
            for entry in suply_imei:
                table.insert("", END,values=(
                    s_no,
                    entry
                    ))
                s_no+=1
        else:
            messagebox.showwarning("Missing Input","Please Select a supplier")                 

    def get_suppliers(self,row):
        filter = {
            "model":str(row[2]),
            "storage":str(row[3]),
            "condition":str(row[5])
        }

        data = self.stock.find_one(filter)
        names = []
        if data:
            name_data = data.get("imei_nos")
            for supplier in name_data.keys():   
                names.append(supplier)

        return names
   
    def save_invoice(self, data, customer, invoice_info, win, on_save=None):

        details = {
            "invoice_no": invoice_info["invoice_no"],
            "inv_date": invoice_info["date"],
            "inv_time": invoice_info["time"],
            "customer_name": customer["name"],
            "customer_cnic": customer["cnic"],
            "payment_type": customer["payment_type"],
            "down_payment": customer["down_payment"],
            "due_date": customer["due_date"],
            "purchased_items": data,
            "total_inv_amount": invoice_info["total_inv_amount"],
            "inv_balance": customer["balance"],
            "profit": invoice_info["profit"],
            "note": invoice_info["note"],
            "returned": False
        }

        details_cr = {
            "inv_date": invoice_info["date"],
            "customer_name": customer["name"],
            "customer_cnic": customer["cnic"],
            "down_payment": customer["down_payment"],
            "due_date": customer["due_date"],
            "total_amount_paid": customer["down_payment"],
            "balance": customer["balance"],
            "status": "unsettled"
        }

        if customer["payment_type"] == "Credit Sale":
            description = f"Received Partial Payment against Invoice no:{invoice_info["invoice_no"]}"
            debit = customer["down_payment"]
        else:
            description =  f"Received Payment against Invoice no:{invoice_info["invoice_no"]}"
            debit = invoice_info["total_inv_amount"]

        balance_find = self.ledger.find_one(sort=[("_id", -1)])
        if balance_find:
            balance = int(balance_find.get("balance",0)) + int(debit)
        else:
            balance = 0 + int(debit)

        ledger_det = {
            "date":invoice_info["date"],
            "description": description,
            "debit":debit,
            "credit":0,
            "balance":balance
        }   

        for item in data:
            filter1 = {
                "model": str(item["model"]),
                "storage": str(item.get("storage", "")),
                "condition": str(item.get("condition", ""))
            }

            stck_find = self.stock.find_one(filter1)

            if not stck_find:
                continue

            if item.get("imei") != "Nill":
                imei_to_delete = item["imei"]
                suppliers_imeis = stck_find.get("imei_nos")

                for supplier, imei_list in suppliers_imeis.items():
                    if imei_to_delete in imei_list:

                        self.stock.update_one(
                            {"_id": stck_find["_id"]},
                            {"$pull": {f"imei_nos.{supplier}": imei_to_delete}}
                        )

                        break

                updated_doc = self.stock.find_one({"_id": stck_find["_id"]})
                updated_imeis = updated_doc.get("imei_nos", {})

                new_quantity = sum(len(v) for v in updated_imeis.values())

            else:
                qty_sold = int(item.get("quantity", 1))
                new_quantity = int(stck_find.get("quantity", 0)) - qty_sold


            self.stock.update_one(
                {"_id": stck_find["_id"]},
                {"$set": {"quantity": new_quantity}}
            )
        
        self.sales.insert_one(details)

        if customer["payment_type"] == "Credit Sale":

            filter_acc = {
                "customer_name": customer["name"],
                "customer_cnic": customer["cnic"]
            }

            acc_find = self.credit_accounts.find_one(filter_acc)

            if acc_find:
                self.credit_accounts.update_one(
                    filter_acc,
                    {
                        "$set": {
                            "down_payment": int(acc_find["down_payment"]) + int(customer["down_payment"]),
                            "total_amount_paid": int(acc_find["total_amount_paid"]) + int(customer["down_payment"]),
                            "balance": int(acc_find["balance"]) + int(customer["balance"]),
                            "due_date": customer["due_date"]
                        }
                    }
                )
            else:
                self.credit_accounts.insert_one(details_cr)

        self.ledger.insert_one(ledger_det)
        messagebox.showinfo("Success", "Invoice Saved successfully!")

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

        entries = self.sales.find().sort("_id", -1)
        s_no =1
        for entry in entries:
            if entry.get("returned") == False or entry.get("return_type") == "Partial Return":
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

    def returned_invoice(self,invoice_no,product,quantity):
        filter={
            "invoice_no":invoice_no
        }
        find = self.sales.find_one(filter)
        purchased_items = find.get("purchased_items")
        for items in purchased_items:
            if items.get("model") == product:
                if items.get("is_mobile") == True:

                    imei = items.get("imei")
                    supplier = items.get("supplier")
                    model = items.get("model")
                    condition = items.get("condition")
                    storage = str(items.get("storage"))
                    
                    filter1 ={
                        "model":model,
                        "condition":condition,
                        "storage":storage
                    }

                    self.stock.update_one(filter1,
                                          {"$addToSet": {f"imei_nos.{supplier}": imei},
                                           "$inc": {"quantity": 1}})

                    item = {
                        "imei": items.get("imei"),
                        "model":  items.get("model"),
                        "storage":  items.get("storage"),
                        "condition":  items.get("condition"),
                        "quantity":  items.get("quantity"),
                        "price":  items.get("price"),
                        "total_amount":  items.get("total_amount"),
                        "is_mobile":  items.get("is_mobile"),
                        "supplier":  items.get("supplier")
                    }

                    self.sales.update_one(filter,{"$pull": {"purchased_items": item}})

                    return_find = self.returned_invoices.find_one(filter)
                    if return_find:
                        purchased_items = return_find.get("purchased_items")
                        purchased_items.append(item)
                        self.returned_invoices.update_one(filter,{"$set":{"purchased_items":purchased_items}})
                    else:
                        purchased_items = items
                        return_finds = find
                        return_finds["purchased_items"] = [purchased_items]
                        self.returned_invoices.insert_one(return_finds)

                elif items.get("is_mobile") == False:        
                    model = items.get("model")

                    filter2 = {
                        "model":model
                    }
                    new_quantity = int(self.stock.find_one(filter2).get("quantity")) + quantity

                    self.stock.update_one(filter2,{"$set": {"quantity": new_quantity}})

                    if items.get("quantity") == quantity:
                        item = {
                            "imei": items.get("imei"),
                            "model":  items.get("model"),
                            "storage":  items.get("storage"),
                            "condition":  items.get("condition"),
                            "quantity":  items.get("quantity"),
                            "price":  items.get("price"),
                            "total_amount":  items.get("total_amount"),
                            "is_mobile":  items.get("is_mobile"),
                            "supplier":  items.get("supplier")
                        }
                    else:
                        item = {
                            "imei": items.get("imei"),
                            "model":  items.get("model"),
                            "storage":  items.get("storage"),
                            "condition":  items.get("condition"),
                            "quantity":  int(items.get("quantity")) - quantity,
                            "price":  items.get("price"),
                            "total_amount":  (int(items.get("quantity")) - quantity)*int(items.get("price")),
                            "is_mobile":  items.get("is_mobile"),
                            "supplier":  items.get("supplier")
                        }

                    self.sales.update_one(filter,{"$pull": {"purchased_items": item}})

                    return_find = self.returned_invoices.find_one(filter)
                    if return_find:
                        purchased_item = return_find.get("purchased_items")
                        purchased_item.append(item)
                        self.returned_invoices.update_one(filter,{"$set":{"purchased_items":purchased_item}})
                    else:
                        purchased_items = items
                        return_find = find
                        return_find["purchased_items"] = [purchased_items]
                        self.returned_invoices.insert_one(return_find)

                total_invoice_amount = find.get("total_inv_amount") - (int(items.get("price"))*quantity)
                self.sales.update_one(filter,{"$set":{"total_inv_amount":total_invoice_amount}})
                break


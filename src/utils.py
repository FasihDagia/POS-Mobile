from tkinter import *
from tkinter import ttk, messagebox,Toplevel,filedialog
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
import os
import sys

def center_window(root,width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(width, height)

def destroy_widgets(root):
    for widget in root.winfo_children():
        widget.destroy()

def create_treeview(parent, columns, widths, height):

    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tree_scroll_y = ttk.Scrollbar(frame, orient="vertical")
    tree_scroll_y.pack(side="right", fill="y")

    tree_scroll_x = ttk.Scrollbar(frame, orient="horizontal")
    tree_scroll_x.pack(side="bottom", fill="x")

    style = ttk.Style()
    style.configure("Treeview",foreground="black",rowheight=20,font=("Helvetica", 9))
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"),rowheight=25) 

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set,
        height=height
    )
    tree.pack(padx=10)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    for col, w in zip(columns, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    tree.tag_configure("oddrow", background="#FFE5B4")   # light peach
    tree.tag_configure("evenrow", background="#FFCBA4")  # darker peach

    original_insert = tree.insert

    def colored_insert(parent, index, values=None, **kwargs):
        row_count = len(tree.get_children())
        tag = "evenrow" if row_count % 2 == 0 else "oddrow"
        return original_insert(parent, index, values=values, tags=(tag,), **kwargs)

    tree.insert = colored_insert

    return tree

def get_selected(tree):
    selected_item = tree.selection()

    if not selected_item:
        return

    row = tree.item(selected_item)["values"]
    return row

def grid_label(root,text,col,ro,fsz):
    ttk.Label(root,text=text,font=("Helvetica",fsz,"bold")).grid(column=col,row=ro,padx=5,pady=7)
    
def grid_create_treeview(parent, columns, widths, height):

    # Main frame (must use grid)
    frame = ttk.Frame(parent)
    frame.grid(sticky="nsew",columnspan=6)

    # Make parent expandable
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    # Make frame expandable
    frame.grid_rowconfigure(0, weight=1)


    # Scrollbars
    tree_scroll_y = ttk.Scrollbar(frame, orient="vertical")
    tree_scroll_x = ttk.Scrollbar(frame, orient="horizontal")

    # Style
    style = ttk.Style()
    style.configure("Treeview", foreground="black", rowheight=20, font=("Helvetica", 9))
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), rowheight=25)

    # Treeview
    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set,
        height=height
    )

    # Layout using grid + columnspan=6
    tree.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

    tree_scroll_y.grid(row=0, column=6, sticky="ns", pady=10)
    tree_scroll_x.grid(row=1, column=0, columnspan=6, sticky="ew", padx=10)

    # Configure scrollbar commands
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    # Column setup
    for col, w in zip(columns, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    # Row colors
    tree.tag_configure("oddrow", background="#FFE5B4")
    tree.tag_configure("evenrow", background="#FFCBA4")

    # Override insert for striped rows
    original_insert = tree.insert

    def colored_insert(parent_item, index, values=None, **kwargs):
        row_count = len(tree.get_children())
        tag = "evenrow" if row_count % 2 == 0 else "oddrow"
        return original_insert(parent_item, index, values=values, tags=(tag,), **kwargs)

    tree.insert = colored_insert

    return tree

def print_invoice(data, customer, invoice_info):

    file_name = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"{invoice_info['invoice_no']}.pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save Invoice As"
    )

    if not file_name:
        return

    doc = SimpleDocTemplate(file_name, pagesize=A4)
    styles = getSampleStyleSheet()

    center_style = ParagraphStyle(
        name="Center",
        parent=styles["Normal"],
        alignment=1
    )

    desc_style = ParagraphStyle(
        name="desc",
        fontSize=9,
        leading=11
    )

    content = []

    # ================= HEADER =================
    content.append(Paragraph("<b>MH POINT</b>", styles["Title"]))
    content.append(Paragraph("<b>The Name of Trust</b>", styles["Title"]))
    content.append(Paragraph(
        "Shop # 242, Street # 11, Block-B, Baldia Complex, Mirpurkhas",
        center_style
    ))
    content.append(Paragraph("Phone: 0336-0601994", center_style))
    content.append(Spacer(1, 20))

    # ================= CUSTOMER + INVOICE =================
    left_data = [
        ["Customer Name:", customer["name"]],
        ["CNIC:", customer["cnic"]],
    ]

    if customer["payment_type"].lower() == "credit sale":
        left_data.append(["Down Payment:", str(customer["down_payment"])])
        left_data.append(["Due Date:", customer["due_date"]])

    right_data = [
        ["Invoice No:", invoice_info["invoice_no"]],
        ["Date:", invoice_info["date"]],
        ["Time:", invoice_info["time"]],
        ["Payment:", customer["payment_type"]],
    ]

    left_table = Table(left_data, colWidths=[120, 150])
    right_table = Table(right_data, colWidths=[120, 150])

    left_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
    ]))

    right_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
    ]))

    info_table = Table([[left_table, right_table]], colWidths=[270, 270])
    info_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    content.append(info_table)
    content.append(Spacer(1, 20))

    # ================= PRODUCT TABLE =================
    table_data = [["S.No", "Description", "QTY", "Price", "Amount"]]

    total = 0

    for i, item in enumerate(data, start=1):

        desc_text = item['model']

        if item.get("storage"):
            desc_text += f" {item['storage']}"
        if item.get("condition"):
            desc_text += f" {item['condition']}"

        # IMEI on next line (cleaner)
        if item.get("imei"):
            desc_text += f"<br/><font size=8>(IMEI: {item['imei']})</font>"

        desc = Paragraph(desc_text, desc_style)

        qty = item["quantity"]
        price = float(item["price"])
        amount = float(item["total_amount"])

        total += amount

        table_data.append([
            i,
            desc,
            qty,
            f"{price:,.0f}",
            f"{amount:,.0f}"
        ])

    # Spacer row
    table_data.append(["", "", "", "", ""])

    # TOTAL row
    table_data.append(["", "", "", "TOTAL", f"{total:,.0f}"])

    # CREDIT SALE
    summary_rows = 1
    if customer["payment_type"].lower() == "credit sale":
        down_payment = float(customer.get("down_payment", 0))
        balance = total - down_payment

        table_data.append(["", "", "", "Down Payment", f"{down_payment:,.0f}"])
        table_data.append(["", "", "", "Balance", f"{balance:,.0f}"])
        summary_rows = 3

    # TABLE
    product_table = Table(
        table_data,
        colWidths=[40, 250, 50, 70, 80]
    )

    # ================= STYLE =================
    style = TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        # Alignments
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
        ("ALIGN", (1, 1), (1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Padding
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

        # Grid for items only
        ("GRID", (0, 0), (-1, -(summary_rows + 2)), 0.5, colors.grey),

        # Summary styling
        ("FONTNAME", (3, -summary_rows), (4, -1), "Helvetica-Bold"),
        ("LINEABOVE", (3, -summary_rows), (4, -summary_rows), 2, colors.black),
    ])

    product_table.setStyle(style)

    content.append(product_table)
    content.append(Spacer(1, 20))

    # ================= NOTE =================
    note_text = invoice_info.get("note", "").strip() or "-"
    content.append(Paragraph("<b>Note:</b>", styles["Heading3"]))
    content.append(Paragraph(note_text, styles["Normal"]))
    content.append(Spacer(1, 20))

    # ================= TERMS =================
    content.append(Paragraph("Terms & Conditions:", styles["Heading3"]))
    content.append(Paragraph("Goods once sold are not returnable.", styles["Normal"]))
    content.append(Paragraph("No warranty of panel on used phones", styles["Normal"]))
    content.append(Paragraph("3 Days checking warranty on used phones", styles["Normal"]))
    content.append(Paragraph(
        "The warranty on the box pack phones is provided by the company, "
        "The shop owner will not be responsible",
        styles["Normal"]
    ))

    content.append(Spacer(1, 40))
    content.append(Paragraph("Signature: HUZAIFA", styles["Normal"]))

    # BUILD PDF
    doc.build(content)

    # PRINT
    os.startfile(file_name, "print")
    
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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def env_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def remove_stock(table,supplier_name,db,filter):
    selected = table.selection()

    if not selected:
        messagebox.showerror("No Selection", "Please select an IMEI to remove")
        return

    confirm = messagebox.askyesno("Remove Stock","Do you want to Remove the item from inventory?")

    if confirm:
        values = table.item(selected)["values"]
        data =  db.find_one(filter)
        quantity = data.get("quantity")
        if quantity == 1:
            db.delete_one(filter)
        else:
            quantity -=1
            imeis = data.get("imei_nos")
            imeis[supplier_name].remove(str(values[1]))
            db.update_one(filter,{"$set":{"quantity":quantity,
                                          "imei_nos":imeis}})


        table.delete(selected)     

    for index, row in enumerate(table.get_children(), start=1):
        values = list(table.item(row, "values"))
        values[0] = index
        table.item(row, values=values)

def validate_frame(frame):
    for child in frame.winfo_children():
        if isinstance(child, ttk.Entry):
            if child.state() == ["!disabled"]:
                if not child.get().strip():
                    return False
    return True

def stk_delete(filter1,selected,dialog,db,table_stocks):
    db.delete_one(filter1)
    table_stocks.delete(selected)     

    for index, row in enumerate(table_stocks.get_children(), start=1):
        values = list(table_stocks.item(row, "values"))
        values[0] = index
        table_stocks.item(row, values=values)

    dialog.destroy()
    messagebox.showinfo("Success","Successfully removed The product from Inventory")

def stk_update(filter1,selected,dialog,db,table_stocks):
    upda = Toplevel(dialog)
    upda.title("Update")
    center_window(upda,300,150)
    upda.maxsize(300, 150)
    upda.grab_set()

    find = db.find_one(filter1)

    entry_frame = Frame(upda)
    entry_frame.pack(pady=10)

    grid_label(entry_frame,"Quantity",0,0,10)
    quan_entry = ttk.Entry(entry_frame,font=("Helvetica",10,"bold"))
    quan_entry.grid(row=0,column=1,padx=5)
    quan_entry.insert(0,find.get("quantity"))

    grid_label(entry_frame,"Purchase Price",0,1,10)
    purchase_price_entry = ttk.Entry(entry_frame,font=("Helvetica",10,"bold"))
    purchase_price_entry.grid(row=1,column=1,padx=5)
    purchase_price_entry.insert(0,find.get("purchase_price"))
    
    ttk.Button(upda,text="Update",cursor="hand2",command=lambda:save()).pack()

    def save():
        quantity = int(quan_entry.get())
        purchase_price = purchase_price_entry.get()
        if not purchase_price or not quantity:
            messagebox.showwarning("Missing Fields","Please Fill the missing fields")
            return
        db.update_one(filter1,{"$set":{"quantity":quantity,"purchase_price":purchase_price}})
        messagebox.showinfo("Success","Successfully updated The product in Inventory")
        upda.destroy()
        dialog.destroy()
        
        item_id = selected[0]
        values = list(table_stocks.item(item_id, "values"))
        values[4] = quantity
        values[6] = purchase_price
        table_stocks.item(item_id, values=values)

def invoice_details(inv_no,db,labels,table):
    invoice = db.find_one({"invoice_no":inv_no})

    if invoice:
        labels["date"].config(text=invoice.get("inv_date"))
        labels["customer_name"].config(text=invoice.get("customer_name"))
        labels["customer_cnic"].config(text=invoice.get("customer_cnic"))
        labels["payment_type"].config(text=invoice.get("payment_type"))
        labels["down_payment"].config(text=invoice.get("down_payment"))
        labels["next_due_date"].config(text=invoice.get("due_date"))
        labels["total_invoice_amount"].config(text=invoice.get("total_inv_amount"))
        labels["note"].config(text=invoice.get("note"))

        for row in table.get_children():
            table.delete(row)
        
        s_no = 1
        for row in invoice.get("purchased_items"):
            table.insert("", END,values=(
                s_no,
                row["imei"],
                row["model"],
                row["storage"],
                row["condition"],
                row["quantity"],
                row["price"],
                row["total_amount"]
            ))
            s_no+=1

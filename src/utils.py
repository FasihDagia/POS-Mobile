from tkinter import *
from tkinter import ttk
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
        print("No row selected")
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

    doc = SimpleDocTemplate(f"{invoice_info["invoice_no"]}.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    center_style = ParagraphStyle(
    name="Center",
    parent=styles["Normal"],
    alignment=1   # 0=left, 1=center, 2=right
)
    content = []
    # ================= COMPANY HEADER =================
    content.append(Paragraph("<b>MH POINT</b>", styles["Title"]))
    content.append(Paragraph("<b>The Name of Trust</b>", styles["Title"]))
    content.append(Paragraph("Shop # 42, Street # 11, Block-B, Baldia Complex, Mirpurkhas", center_style))
    content.append(Paragraph("Phone: 0336-0601994", center_style))
    content.append(Spacer(1, 20))

    # ================= CUSTOMER + INVOICE SECTION =================
    left_data = [
        ["Customer Name:", customer["name"]],
        ["CNIC:", customer["cnic"]],
    ]

    # Add credit details if needed
    if customer["payment_type"].lower() == "credit sale":
        left_data.append(["Down Payment:", str(customer["down_payment"])])
        left_data.append(["Due Date:", customer["due_date"]])

    right_data = [
        ["Invoice No:", invoice_info["invoice_no"]],
        ["Date:", invoice_info["date"]],
        ["Time:", invoice_info["time"]],
        ["Payment:", customer["payment_type"]],
    ]

    table_data = [
        [Table(left_data), Table(right_data)]
    ]

    table = Table(table_data, colWidths=[270, 270])
    content.append(table)
    content.append(Spacer(1, 20))

    # ================= PRODUCTS TABLE =================
    table_data = [["S.No", "Description", "Amount"]]

    total = 0

    for i, item in enumerate(data, start=1):
        desc = f"{item['model']} {item['storage']} {item['condition']} (IMEI: {item['imei']})"
        amount = item["price"]

        total += amount

        table_data.append([i, desc, amount])

    # Add total row
    table_data.append(["", "TOTAL", total])

    product_table = Table(table_data, colWidths=[50, 350, 100])

    product_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (2,1), (-1,-1), "RIGHT"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ]))

    content.append(product_table)
    content.append(Spacer(1, 30))

    # ================= FOOTER =================
    content.append(Paragraph("Terms & Conditions:", styles["Heading3"]))
    content.append(Paragraph("Goods once sold are not returnable.", styles["Normal"]))
    content.append(Paragraph("No warranty of panel on used phones", styles["Normal"]))
    content.append(Paragraph("3 Days checking warranty on used phones", styles["Normal"]))
    content.append(Paragraph("The warranty on the box pack phones is provided by the company, The shop owner will not be responsible", styles["Normal"]))
     
    content.append(Spacer(1, 50))

    content.append(Paragraph("Signature: ____________________", styles["Normal"]))

    # ================= BUILD =================
    doc.build(content)

    # Auto print
    os.startfile(f"{invoice_info["invoice_no"]}.pdf", "print")
    
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
import tkinter as tk
from tkinter import ttk
import win32print
from datetime import datetime

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

MAX_WIDTH = 32   # 32 (58mm) or 48 (80mm)
def center(text):
    return text.center(MAX_WIDTH)

def line():
    return "-" * MAX_WIDTH

def left_right(left, right):
    return left + " " * (MAX_WIDTH - len(left) - len(right)) + right

def format_row(sno, imei, model, price):
    sno_w = 4
    imei_w = 10
    price_w = 8
    model_w = MAX_WIDTH - sno_w - imei_w - price_w

    imei = str(imei)[:imei_w]
    model = str(model)[:model_w]

    return f"{sno:<{sno_w}}{imei:<{imei_w}}{model:<{model_w}}{price:>{price_w}}"

def print_invoice(data, invoice_no, payment_type):
    invoice = ""

    # ===== SHOP HEADER =====
    invoice += center("MH Point") + "\n"
    invoice += line() + "\n"

    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M")

    invoice += left_right("Invoice:", str(invoice_no)) + "\n"
    invoice += left_right("Date:", date) + "\n"
    invoice += left_right("Time:", time) + "\n"
    invoice += left_right("Payment:", payment_type[0]) + "\n"
    if payment_type[0] == "Credit Sale":
        invoice += left_right("Down Payment:", payment_type[1]) + "\n"
        invoice += left_right("Due Date:", payment_type[2]) + "\n"

    invoice += line() + "\n"

    invoice += format_row("No", "IMEI", "Model", "Price") + "\n"
    invoice += line() + "\n"

    total = 0

    for i, item in enumerate(data, start=1):
        imei = item["imei"]
        model = f"{item['model']} {item['storage']} {item['condition']}"
        price = item["price"]

        total += price

        invoice += format_row(i, imei, model, price) + "\n"

    invoice += line() + "\n"
    invoice += left_right("TOTAL", str(total)) + "\n"
    invoice += line() + "\n"
    invoice += center("Thank You!") + "\n"
    invoice += center("Visit Again") + "\n\n\n"

    invoice += "\x1d\x56\x00"

    printer_name = win32print.GetDefaultPrinter()
    handle = win32print.OpenPrinter(printer_name)

    job = win32print.StartDocPrinter(handle, 1, ("Invoice", None, "RAW"))
    win32print.StartPagePrinter(handle)

    win32print.WritePrinter(handle, invoice.encode("utf-8"))

    win32print.EndPagePrinter(handle)
    win32print.EndDocPrinter(handle)
    win32print.ClosePrinter(handle)

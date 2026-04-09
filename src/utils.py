import tkinter as tk
from tkinter import ttk

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
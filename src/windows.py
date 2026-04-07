from tkinter import ttk,messagebox
from src.database import database


class windows:
        
    def __init__(self,root):
        self.root = root
        self.db = database(self.root)

    def home_page(self):
        self.root.geometry("900x700")
        self.root.title("HomePage")
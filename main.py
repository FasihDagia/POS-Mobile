import tkinter as tk
from src.windows import windows
from src.utils import resource_path
def main():
    root = tk.Tk()
    win = windows(root)
    root.iconbitmap(resource_path("assets/point-of-sale.ico"))
    win.landing_page()
    root.mainloop()


if __name__ == "__main__":
    main()

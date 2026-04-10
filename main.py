import tkinter as tk
from src.windows import windows
def main():
    root = tk.Tk()
    win = windows(root)
    # win.landing_page()
    # win.home_page()
    win.stocks_window()
    root.mainloop()


if __name__ == "__main__":
    main()

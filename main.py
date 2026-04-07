import tkinter as tk
from src.windows import windows
def main():
    root = tk.Tk()
    win = windows(root)
    win.home_page()
    root.mainloop()


if __name__ == "__main__":
    main()

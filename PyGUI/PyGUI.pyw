import tkinter as tk
import tkinter.ttk as ttk
import GUIForm
import sys

def main():
    global window
    global _form

    print("You are using Python {}.{}.{}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))

    window=tk.Tk()
    GUIForm.BuildInterface(window)
    window.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from GUI import AppGUI
from tkinter import ttk
import os
import json
from datetime import datetime
import shutil
import subprocess
import psutil
from config import *




def main():
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from login import LoginFrame

def start_dashboard(username, role):
    from dashboard.dashboard import Dashboard
    Dashboard(root, username, role)

root = tk.Tk()
root.state('zoomed')
root.title("BengkelKu")

LoginFrame(root, start_dashboard)

root.mainloop()

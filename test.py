from main_classes import *
from GUI import *

# Runs the program entirely and loops until it ends.
if __name__ == "__main__":
    root = tk.Tk()
    app = CompanySystemGUI(root)
    root.mainloop()


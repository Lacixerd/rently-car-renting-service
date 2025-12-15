import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'gui')))
from gui.app import RentalApp

if __name__ == "__main__":
    app = RentalApp()
    app.mainloop()
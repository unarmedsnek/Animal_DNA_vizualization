"""
This is the main file for the application. It initializes the database and the GUI.
"""

import db
import gui

if __name__ == "__main__":
    db.db_init()
    gui.gui_init()
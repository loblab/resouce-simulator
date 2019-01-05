#!/usr/bin/python3
import sys
from sim_app import SimApp

ID = "resim"
DESC = "Resource simulator"

class App(SimApp):
    pass

if __name__ == "__main__":
    app = App(ID, DESC)
    sys.exit(app.main())


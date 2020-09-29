import sqlite3

class database:
    def __init__(self,):

        with sqlite3.connect("db/trials.db") as self.db:
            self.cur = self.db.cursor()
import numpy as np
if __name__ == "__main__":
    pass
import unittest
import os, sys, sqlite3, datetime

from database_methods import signUpUser,findTasks,signInUser,tasksList,newTask,editTasks,editTaskss,undoComplete,deleteTask,completeTasks,viewTasks,completedList
dirname = os.path.dirname(sys.argv[0])
from user import User


class TestStringMethods(unittest.TestCase):
    
    def test_init_mail_error(self):
        with self.assertRaises(ValueError):
            User("","","nesto")
            
    def test_init_username_error(self):
        with self.assertRaises(ValueError):
            User("m maras","","")
            
    def test_init_password_error(self):
        with self.assertRaises(ValueError):
            User("","123","")

    def test_init_newTask(self):
        newTask(1,"First task","This is my first task","","No","")
        con=sqlite3.connect('data\\todo.db')
        cur=con.cursor()

        idd=cur.execute('SELECT * FROM sqlite_sequence').fetchall()
        print("Ovo je idd")
        print(idd)
        seq=idd[1][1]
        print("ovo je seq:")
        print(seq)
        row=cur.execute('SELECT * FROM todo WHERE id=(?)',(seq,)).fetchone()
        self.assertEqual(row,(seq,"1","First task","This is my first task","","No",""))
        podaci=(seq,"1","First task","This is my first task","","No","")
        print("Ovo je rezultat:")
        print(row)
        print("Ovo je unos:")
        print(podaci)
        con=sqlite3.connect('data\\todo.db')
        cur=con.cursor()
        cur.execute('DELETE FROM todo WHERE id=?',(seq,))
        con.commit()
   

if __name__ == '__main__':
    unittest.main()

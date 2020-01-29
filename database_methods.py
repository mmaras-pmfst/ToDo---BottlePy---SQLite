import sqlite3
import os, sys

dirname = os.path.dirname(sys.argv[0])
sys.path.append(dirname.replace('\\', '/') + '/entiteti/')

from user import User
from todo import Todo

def signUpUser(username,password1,password2,email):
    con=sqlite3.connect('data\\todo.db')
    testing=False
    idd=0
    try:
        cur=con.cursor()
        cur.execute('SELECT username FROM user WHERE username= ?',(username,))
        test=cur.fetchone()
        
        if test==None:
            if password1==password2:
                #DATABASE QUERY
                cur.execute('INSERT INTO user VALUES (null,?,?,?)',(username,password1,email))
                con.commit()
                
                cur.execute('SELECT * FROM user WHERE username= ?',(username,))
                nesto=cur.fetchone()
                
                idd=nesto[0]
                
                testing=True
                print("You have created an account!")
            else:
                testing=False
                print("Passwords are not matching!")
        else:
            testing=False
            print("Username already exists!")
            
    except Exception as e:
        print("Error at signUpUser: ",e)
        con.rollback
        
    con.close()
    return (testing,idd)

def signInUser(username,password):
    con=sqlite3.connect('data\\todo.db')
    testing=False
    idd=0
    try:
        cur=con.cursor()
        id1=cur.execute('SELECT * FROM user WHERE username = (?) AND password = (?)',(username,password,))
        
        id1=cur.fetchone()
        print("Ovo je id1:")
        print(id1)
        if id1!=None:
            idd=id1[0]
            print("Correct username and password")
            testing=True
        else:
            print("Wrong password or username")
            testing=False
    except Exception as e:
        print("Error at signInUser: ",e)
        con.rollback
    con.close()
    return (testing,idd)

def tasksList(save_id):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        complete="No"
        cur.execute('SELECT * FROM todo WHERE user_id= (?) AND datetime_complete= (?) ORDER BY datetime DESC',(save_id,complete,)) 
        rows=cur.fetchall()
        print("All data from selected user:")
        print(rows)
        print("Current user id: "+str(save_id))
        #DATABASE QUERY FOR user TABLE
        cur.execute('SELECT * FROM user WHERE id=(?)',(save_id,))
        data=cur.fetchone()[1]
        print("Current username is:")
        print(data)
        
    except Exception as e:
        print("Error at tasksList: ",e)
        con.rollback
    con.close()
    return (data,rows)

def tasksList2(save_id):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        complete="No"
        cur.execute('SELECT * FROM todo WHERE user_id= (?) AND datetime_complete= (?) ORDER BY datetime ASC',(save_id,complete,)) 
        rows=cur.fetchall()
        print("All data from selected user:")
        print(rows)
        print("Current user id: "+str(save_id))
        #DATABASE QUERY FOR user TABLE
        cur.execute('SELECT * FROM user WHERE id=(?)',(save_id,))
        data=cur.fetchone()[1]
        print("Current username is:")
        print(data)
        
    except Exception as e:
        print("Error at tasksList: ",e)
        con.rollback
    con.close()
    return (data,rows)

def findTasks(keyword,save_id):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY
        cur.execute('SELECT * FROM todo WHERE user_id= ? AND title LIKE ?',(save_id,"%"+keyword+"%",))
        rows=cur.fetchall()
        print("Search resault:")
        print(rows)
        cur.execute('SELECT * FROM user WHERE id=(?)',(save_id,))
        data=cur.fetchone()[1]
        print("Current username is:")
        print(data)
        
    except Exception as e:
        print("Error at findTasks: ",e)
        con.rollback
    con.close()
    return (data,rows)
    
   
def newTask(save_id,todotitle,tododesc,tododatetime,complete,timetable):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY       
        cur.execute('INSERT INTO todo VALUES (null,?,?,?,?,?,?)',(save_id,todotitle,tododesc,tododatetime,complete,timetable))
        con.commit()
        
    except Exception as e:
        print("Error at newTask: ",e)
        con.rollback
    con.close()

def editTasks(todotitle,tododesc,tododatetime,todotimetable,changeitem):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY       
        cur.execute('UPDATE todo SET title=(?),desc=(?),datetime=(?),timetable=(?) WHERE id=(?)',(todotitle,tododesc,tododatetime,todotimetable,changeitem,))
        con.commit()
        
    except Exception as e:
        print("Error at editTasks: ",e)
        con.rollback
    con.close()

def editTaskss(changeitem):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY
        cur.execute('SELECT * FROM todo WHERE id=(?)',(changeitem,))    
        result=cur.fetchone()
        
    except Exception as e:
        print("Error at editTaskss: ",e)
        con.rollback
    con.close()
    return result

def undoComplete(returnitem,complete):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY
        cur.execute('UPDATE todo SET datetime_complete= (?) WHERE id = (?)',(complete,returnitem,))
        con.commit()
        
    except Exception as e:
        print("Error at undoComplete: ",e)
        con.rollback
    con.close()

def deleteTask(deleteitem):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY
        cur.execute('DELETE FROM todo WHERE id = (?)',(deleteitem,))
        con.commit()
        
    except Exception as e:
        print("Error at deleteTask: ",e)
        con.rollback
    con.close()

def completeTasks(comp,completeitem):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY
        cur.execute('UPDATE todo SET datetime_complete= (?) WHERE id = (?)',(comp,completeitem,))
        con.commit()
        
    except Exception as e:
        print("Error at completeTasks: ",e)
        con.rollback
    con.close()

def viewTasks(idd):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        cur.execute('SELECT * from todo WHERE id=(?)',(idd,))
        result=cur.fetchone()    
    
    except Exception as e:
        print("Error at viewTasks: ",e)
        con.rollback
    con.close()
    return result

def completedList(save_id,complete):
    con=sqlite3.connect('data\\todo.db')    
    try:
        cur=con.cursor()
        #DATABASE QUERY
        cur.execute('SELECT * FROM todo WHERE user_id= (?) AND datetime_complete= (?) ORDER BY datetime ASC',(save_id,complete,)) 
        rows=cur.fetchall()
        print("All data from selected user:")
        print(rows)
        print("Current user id: "+str(save_id))
           
    
    except Exception as e:
        print("Error at completedList: ",e)
        con.rollback
    con.close()
    return rows


    
    
    
    
    
    
    
    
    
        
    
    
        
        

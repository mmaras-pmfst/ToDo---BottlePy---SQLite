from bottle import Bottle, redirect, run, \
     template, debug, get, route, static_file, request, post

import os, sys, sqlite3, datetime

dirname = os.path.dirname(sys.argv[0])

#CONNECT DATABASE
con=sqlite3.connect('data\\todo.db')
cur=con.cursor()
save_id=0

app = Bottle()
debug(True)


@app.route('/static/<filename:re:.*\.png>')
def send_png(filename):
    return static_file(filename, root=dirname+'/static/assets/img')

@app.route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/assets/css')

@app.route('/static/<filename:re:.*\.css.map>')
def send_cssmap(filename):
    return static_file(filename, root=dirname+'/static/assets/css')

@app.route('/static/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root=dirname+'/static/assets/js')

@app.route('/static/<filename:re:.*\.js.map>')
def send_jsmap(filename):
    return static_file(filename, root=dirname+'/static/assets/js')
    

@app.route('/signUp',method=['GET','POST'])
def signUp():
    if request.POST.get('register','').strip():
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        cur.execute('SELECT username FROM user WHERE username= ?',(username,))
        test=cur.fetchone()
        print(test)
        if test==None:
            if password1==password2:
                #DATABASE QUERY
                cur.execute('INSERT INTO user VALUES (null,?,?,?)',(username,password1,email))
                con.commit()
                cur.execute('SELECT * FROM user WHERE username = (?)',(username,))
                id_user=cur.fetchone()[0]
                print("User id is:")
                print(id_user)
                global save_id
                save_id=id_user
                redirect('/tasks')
            else:
                print("Wrong password")
                return template('signUp')
        else:
            print("Username already exists!")
            return template('signUp')
    else:
        return template('signUp')

@app.route('/lostPassword')
def lostPassword():    
    return template('lostPassword')

@app.route('/logOut')
def logOut():
    redirect('/')

@app.route('/completedTasks')
def completedTasks():
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/tasks' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/tasks' IT WILL REDIRECT US TO '/'
    #DATABASE QUERY
    complete="Yes"
    cur.execute('SELECT * FROM todo WHERE user_id= (?) AND datetime_complete= (?) ORDER BY datetime ASC',(save_id,complete,)) 
    rows=cur.fetchall()
    print("All data from selected user:")
    print(rows)
    print("Current user id: "+str(save_id))
    
    return template('completedTasks',rows=rows)

@app.route('/signIn',method=['GET','POST'])
def signIn():
    if request.POST.get('login','').strip():
        username=request.POST.get('username')
        password=request.POST.get('password')
        id1=cur.execute('SELECT * FROM user WHERE username = (?) AND password = (?)',(username,password,))
        id1=cur.fetchone()
        print("Does user exists:")
        print(id1)        
        if id1!=None:
            global save_id
            save_id=id1[0]
            print("Sign in id: "+str(save_id))
            redirect('/tasks')
        else:
            return template('signIn')      
    else:
        return template('signIn')

@app.route('/item<item:re:[0-9]+>')
def viewtask(item):
    idd=item
    print("Ulazi u def viewtask")
    cur.execute('SELECT * from todo WHERE id=(?)',(idd,))
    result=cur.fetchone()
    global save_id
    save_id=result[1]
    title=result[2]
    desc=result[3]
    datetimee=convDate=datetime.datetime.strptime(result[4],"%Y-%m-%d %H:%M:%S.%f").strftime("%A %d %B %Y - %I:%M %p")
    return template('viewtask',title=title,desc=desc,datetimee=datetimee)

@app.route('/complete<complete:re:[0-9]+>')
def complete_task(complete):
    completeitem=complete
    comp="Yes"
    #DATABASE QUERY
    cur.execute('UPDATE todo SET datetime_complete= (?) WHERE id = (?)',(comp,completeitem,))
    con.commit()
    redirect('/tasks')
   
@app.route('/delete<delete:re:[0-9]+>')
def delete_task(delete):
    deleteitem=delete
    #DATABASE QUERY
    cur.execute('DELETE FROM todo WHERE id = (?)',(deleteitem,))
    con.commit()    
    redirect('/tasks')
    
@app.route('/deletee<deletee:re:[0-9]+>')
def delete_task(deletee):
    deleteitem=deletee
    #DATABASE QUERY
    cur.execute('DELETE FROM todo WHERE id = (?)',(deleteitem,))
    con.commit()    
    redirect('/completedTasks')

@app.route('/reeturn<reeturn:re:[0-9]+>')
def return_task(reeturn):
    returnitem=reeturn
    complete="No"
    #DATABASE QUERY
    cur.execute('UPDATE todo SET datetime_complete= (?) WHERE id = (?)',(complete,reeturn,))
    con.commit()
    redirect('/completedTasks')

@app.route('/new',method=['GET','POST'])  
def new_task():
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/new' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/new' IT WILL REDIRECT US TO '/'
    if request.POST.get('save','').strip():
        todotitle=request.POST.get('task')
        tododesc=request.POST.get('desc')
        tododatetime=datetime.datetime.now()
        complete='No'
        #DATABASE QUERY       
        cur.execute('INSERT INTO todo VALUES (null,?,?,?,?,?)',(save_id,todotitle,tododesc,tododatetime,complete))
        con.commit()        
        redirect('/tasks')
    else:    
        return template('newtask')

@app.route('/tasks')
def index():
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/tasks' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/tasks' IT WILL REDIRECT US TO '/'
    #DATABASE QUERY FOR todo TABLE
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
    
    return template('index', data = data,rows=rows)



@app.route('/')
def title():    
    global save_id
    save_id=0
    print("Initialized save_id:")
    print(save_id)
    return template('titlePage')

run(app, host='localhost', port = 1223, debug='True', reloader='True')

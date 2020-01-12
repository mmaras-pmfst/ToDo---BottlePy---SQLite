from bottle import Bottle, redirect, run, \
     template, debug, get, route, static_file, request, post

import os, sys, sqlite3, datetime

dirname = os.path.dirname(sys.argv[0])

#CONNECT DATABASE
con=sqlite3.connect('data\\todo.db')
cur=con.cursor()

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
    
@app.route('/delete<delete:re:[0-9]+>')
def delete_task(delete):
    deleteitem=delete    
    cur.execute('DELETE FROM todo WHERE id = (?)',(deleteitem,))
    con.commit()
    redirect('/tasks')

@app.route('/new',method=['GET','POST'])  
def new_task():
    if request.POST.get('save','').strip():
        todotitle=request.POST.get('task')
        tododesc=request.POST.get('desc')
        tododatetime=datetime.datetime.now()
        global save_id
        complete='No'
        #DATABASE QUERY       
        cur.execute('INSERT INTO todo VALUES (null,?,?,?,?,?)',(save_id,todotitle,tododesc,tododatetime,complete))
        con.commit()        
        redirect('/tasks')
    else:    
        return template('newtask')

@app.route('/tasks')
def index():
    #DATABASE QUERY
    global save_id
    cur.execute('SELECT * FROM todo WHERE user_id= (?) ORDER BY datetime ASC',(save_id,)) 
    rows=cur.fetchall()
    print("All data from selected user:")
    print(rows)
    print("Current user id: "+str(save_id))
    data = {"developer_name": "PMF student",
            "developer_organization": "PMF"}
    return template('index', data = data,rows=rows)



@app.route('/')
def title():    
    global save_id
    save_id=0
    print("Initialized save_id:")
    print(save_id)
    return template('titlePage')

run(app, host='localhost', port = 1234,debug='True',reloader='True')

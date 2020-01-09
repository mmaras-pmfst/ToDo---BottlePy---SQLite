from bottle import Bottle, redirect, run, \
     template, debug, get, route, static_file, request, post

import os, sys, sqlite3, datetime

dirname = os.path.dirname(sys.argv[0])
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

@app.route('/delete<delete:re:[0-9]+>')
def delete_task(delete):
    deleteitem=delete
    
    cur.execute('DELETE FROM todo WHERE id = (?)',deleteitem)
    con.commit()
    rows=cur.execute('SELECT * FROM todo ORDER BY datetime ASC')
    redirect('/tasks')

@app.route('/new',method=['GET','POST']) #Novo dodano 
def new_task():
    if request.POST.get('save','').strip():
        todotitle=request.POST.get('task')
        tododesc=request.POST.get('desc')
        tododatetime=datetime.datetime.now()
        id_user='1'
        complete='No'

        #CONNECT DATABASE
        
        cur.execute('INSERT INTO todo VALUES (null,?,?,?,?,?)',(id_user,todotitle,tododesc,tododatetime,complete))
        con.commit()
        rows=cur.execute('SELECT * FROM todo ORDER BY datetime ASC')
        
        redirect('/tasks')
    else:    
        return template('newtask')

@app.route('/tasks')
def index():
    #CONNECT DATABASE
    
    rows=cur.execute('SELECT * FROM todo ORDER BY datetime ASC') #Novo
    data = {"developer_name": "PMF student",
            "developer_organization": "PMF"}
    return template('index', data = data,rows=rows)

@app.route('/signUp')
def signUp():
    return template('signUp')

@app.route('/lostPassword')
def lostPassword():
    return template('lostPassword')

@app.route('/signIn')
def signIn():
    return template('signIn')

@app.route('/')
def title():    
    return template('titlePage')

run(app, host='localhost', port = 1234,debug='True',reloader='True')

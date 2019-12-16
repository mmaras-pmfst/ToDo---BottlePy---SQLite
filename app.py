from bottle import Bottle, run, \
     template, debug, get, route, static_file, request, post

import os, sys, sqlite3, datetime

dirname = os.path.dirname(sys.argv[0])

app = Bottle()
debug(True)

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

@app.route('/new',method=['GET','POST']) #Novo dodano 
def new_task():
    if request.POST.get('save','').strip():
        todotitle=request.POST.get('task')
        tododesc=request.POST.get('desc')
        tododatetime=datetime.datetime.now()

        #CONNECT DATABASE
        con=sqlite3.connect('data\\todo.dat')
        cur=con.cursor()
        rec=cur.execute('INSERT INTO todo VALUES (null,?,?,?)',(todotitle,tododesc,tododatetime))
        con.commit()
        rows=cur.execute('SELECT * FROM todo ORDER BY datetime ASC')

        return template("index",rows=rows)
    else:    
        return template('newtask')

@app.route('/tasks')
def index():
    #CONNECT DATABASE
    con=sqlite3.connect('data/todo.dat') #Novo
    cur=con.cursor() #Novo
    rows=cur.execute('SELECT * FROM todo ORDER BY datetime ASC') #Novo
    data = {"developer_name": "PMF student",
            "developer_organization": "PMF"}
    return template('index', data = data,rows=rows)

@app.route('/')
def title():    
    return template('titlePage')

run(app, host='localhost', port = 4040,debug='True',reloader='True')

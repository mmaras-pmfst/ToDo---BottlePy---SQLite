from bottle import Bottle, redirect, run, \
     template, debug, get, route, static_file, request, post

import os, sys, sqlite3, datetime
from database_methods import signUpUser,findTasks,signInUser,tasksList2,tasksList,newTask,editTasks,editTaskss,undoComplete,deleteTask,completeTasks,viewTasks,completedList
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
        test=signUpUser(username,password1,password2,email)
        if test[0]==False:
            return template('signUp')
        else:
            global save_id
            save_id=test[1]
            redirect('/tasks')
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
    complete="Yes"
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/tasks' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/tasks' IT WILL REDIRECT US TO '/'
    rows=completedList(save_id,complete)
    
    return template('completedTasks',rows=rows)

@app.route('/signIn',method=['GET','POST'])
def signIn():
    if request.POST.get('login','').strip():
        username=request.POST.get('username')
        password=request.POST.get('password')
        testing=signInUser(username,password)
        if testing[0]==True:
            global save_id
            save_id=testing[1]
            redirect('/tasks')
        else:
            return template('signIn')
              
    else:
        return template('signIn')

@app.route('/item<item:re:[0-9]+>')
def viewtask(item):
    idd=item
    result=viewTasks(idd)
    global save_id
    save_id=result[1]
    title=result[2]
    desc=result[3]
    x=result[6]
    timetable=x.replace("T"," ")
    datetimee=convDate=datetime.datetime.strptime(result[4],"%Y-%m-%d %H:%M:%S.%f").strftime("%A %d %B %Y - %I:%M %p")
    return template('viewtask',title=title,desc=desc,datetimee=datetimee,timetable=timetable)

@app.route('/complete<complete:re:[0-9]+>')
def complete_task(complete):
    completeitem=complete
    comp="Yes"
    completeTasks(comp,completeitem)
    redirect('/tasks')
   
@app.route('/delete<delete:re:[0-9]+>')
def delete_task(delete):
    deleteitem=delete
    deleteTask(deleteitem)   
    redirect('/tasks')
    
@app.route('/deletee<deletee:re:[0-9]+>')
def delete_task(deletee):
    deleteitem=deletee
    deleteTask(deleteitem)    
    redirect('/completedTasks')

@app.route('/reeturn<reeturn:re:[0-9]+>')
def return_task(reeturn):
    returnitem=reeturn
    complete="No"
    undoComplete(returnitem,complete)
    redirect('/completedTasks')

@app.route('/change<change:re:[0-9]+>',method=['GET','POST'])
def change(change):
    changeitem=change
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/change' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/new' IT WILL REDIRECT US TO '/'
    if request.POST.get('change','').strip():
        print("button change is pressed")
        todotitle=request.POST.get('taskk')
        tododesc=request.POST.get('descc')
        todotimetable=request.POST.get('timetablee')
        tododatetime=datetime.datetime.now()
        complete='No'
        editTasks(todotitle,tododesc,tododatetime,todotimetable,changeitem)        
        redirect('/tasks')      
    else:        
        result=editTaskss(changeitem)        
        save_id=result[1]
        title=result[2]
        desc=result[3]
        timetable=result[6]
        return template('updateTask',title=title,desc=desc,changeitem=changeitem,timetable=timetable)
    

@app.route('/new',method=['GET','POST'])  
def new_task():
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/new' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/new' IT WILL REDIRECT US TO '/'
    if request.POST.get('save','').strip():
        todotitle=request.POST.get('task')
        tododesc=request.POST.get('desc')
        timetable=request.POST.get('timetable')
        tododatetime=datetime.datetime.now()
        complete='No'
        newTask(save_id,todotitle,tododesc,tododatetime,complete,timetable)
                
        redirect('/tasks')
    else:    
        return template('newtask')

@app.route('/tasks',method=['GET','POST'])
def index():
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/tasks' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/tasks' IT WILL REDIRECT US TO '/'
    testing=tasksList(save_id)
    data=testing[0]
    rows=testing[1]    
    return template('index', data = data,rows=rows,form_action="/search")

@app.route('/taskss',method=['GET','POST'])
def index():
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/tasks' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/tasks' IT WILL REDIRECT US TO '/'
    
    testing=tasksList2(save_id)
    data=testing[0]
    rows=testing[1]    
    return template('index', data = data,rows=rows,form_action="/search")

@app.route('/search',method=['POST'])
def search():
    global save_id
    if save_id==0:
        redirect('/') #IF WE WERE ON ROUTE '/tasks' AND WE STOP THE SERVER AND START IT AGAIN, THEN REFRESH '/tasks' IT WILL REDIRECT US TO '/'
    keyword=request.forms.get('word')
    result=findTasks(keyword,save_id)
    data=result[0]
    rows=result[1]
    return template('index', data = data,rows=rows,form_action="/search")
    
    

@app.route('/')
def title():    
    global save_id
    save_id=0
    print("Initialized save_id:")
    print(save_id)
    return template('titlePage')

run(app, host='localhost', port = 1224, debug='True', reloader='True')

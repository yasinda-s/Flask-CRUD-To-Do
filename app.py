from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #the database that will be used
db = SQLAlchemy(app)

class Todo(db.Model): #create a class for the database
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): #how the object will be printed in the terminal
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET']) #the landing page can now accept POST and GET requests
def index(): #the function that will run with the route /
    if request.method == 'POST': #if the request sent to "/" is a POST request (if user fills form to add task)
        task_content = request.form['content'] #get the content of the task from the form
        new_task = Todo(content=task_content) #make an instance of the Todo class with the content
        try:
            db.session.add(new_task) #add the new task to the database
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #get all the tasks from the database
        return render_template('index.html', tasks=tasks) #render the index.html template with the tasks
    
@app.route('/delete/<int:id>') #the route to delete a task with the id passed in the url
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #get the task with the id passed in the url
    try:
        db.session.delete(task_to_delete) #delete the task with the id passed in the url
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    

@app.route('/update/<int:id>', methods=['GET', 'POST']) #the route to update a task with the id passed in the url
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST': #request is used to get the form data
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task'
    else:
        return render_template('update.html', task=task_to_update) #if there is a post request, the task will be updated, if not, the update.html template will be rendered with the task
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
# Importing the Flask class from the flask module.
from flask import Flask, render_template,request,redirect,url_for,jsonify

# Importing the SQLAlchemy class from the flask_sqlalchemy module.
from flask_sqlalchemy import SQLAlchemy;


# Creating a new instance of the Flask class for our web app.
app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# import pdb; pdb.set_trace()


# config file for db 
uri = 'postgresql://postgres:7y8a1h64@localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] =  uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initializing a db instance
db = SQLAlchemy(app)
# model blueprint for todo app
class Todo(db.Model):
  # __tablename__ = 'todos'
  id = db.Column(db.Integer,primary_key=True)
  description = db.Column(db.String(),nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# Creating the table in the database.
db.create_all()


@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
   description = request.get_json()['description']
   todo = Todo(description=description)
   db.session.add(todo)
   db.session.commit()
   body['id'] = todo.id
   body['completed'] = todo.completed
   body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
      completed = request.get_json()['completed']
      todo = Todo.query.get(todo_id)
      todo.completed = completed
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('index'))


@app.route('/')
def index():
  return render_template('index.html',data=Todo.query.all())
   












# # A way to run the app on a local server.
# if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=3000)
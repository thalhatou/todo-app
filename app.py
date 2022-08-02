from flask import Flask, render_template
# sql alchemy 
from flask_sqlalchemy import SQLAlchemy;
app = Flask(__name__)

# 

# config file for db 
# 
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

db.create_all()

  """
  It returns the index.html file and passes the data from the database to the index.html file.
  :return: The index.html template is being returned.
  """
@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.all())












#always include this at the bottom of your code (port 3000 is only necessary in workspaces)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=3000)
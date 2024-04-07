# ---- BASIC FLASK APPLICATION ------

# also need to define some environmental variables with every terminal....  
# enter these into powershell (equivalent to linux "export")
#   $env:FLASK_APP = 'application.py'
#   $env:FLASK_ENV = 'development' 
# double check this worked with command
#   Get-Childitem -path env:FLASK_APP

# Then to start the flask application in powershell: 
#   flask run
# Then you can open the site (it will tell you the URL)
#
# you can populate the db with inline python-
#   from application import db
#   from application import Drink
#   drink = Drink(name="Grape Soda", description = "tastes like grapes")
# Now if cmd drink, it will return: Grape Soda - tastes like grapes

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# configure our database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# create the db instance using our app
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    # in CMD python, if you type "drink", it will return the drink db info
    def __repr__(self):
        return f"{self.name} - {self.description}"
    
# create the drinks - comment out this part after running for the first time!!! 
# otherwise it will error because what it is trying to add is no longer unique
# with app.app_context():
#     db.create_all()
#     db.session.add(Drink(name="Grape Soda", description = "tastes like grapes"))
#     db.session.add(Drink(name="Cherry Soda", description = "tastes like cherry ice cream"))
#     db.session.commit()

# method returned when someone visits this route (aka the index or home landing page)
@app.route('/')
def index():
    return 'Hello!'

# method returned when someone visits this route (aka the drinks page)
# this can be singular or plural.... seems like it usually should be singular but it's plural here, k?
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

    return {"drinks": output}

# http://127.0.0.1:5000/drinks/1 for example
@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id) 
    return jsonify({"name": drink.name, "description": drink.description})


# adding a new drink
# this is easier to test in Postman!
# make a new HTTP request, type POST, url http://127.0.0.1:5000/drinks
# in the body, choose "raw" then put in: 
#   {
#       "name":"Cola",
#       "description": "delicious"
#   }
# then press SEND and you should see it return the new id!
# feel free to check all drinks now by changing type to GET and sending that
@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

# deleting a drink
# in Postman, type DELETE, url http://127.0.0.1:5000/drinks/3 or the ID
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)

    if drink is None:
        return {"error" : "404 not found"}
    
    db.session.delete(drink)
    db.session.commit()

    return {"message": "yeet!"}

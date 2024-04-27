from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('users', lazy=True))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', categories=Category.query.all())
    elif request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        category_id = request.form['category']
        new_user = User(firstname=firstname, lastname=lastname, email=email, password=password, category_id=category_id)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/account')
def account():
    return render_template('account.html', categories=Category.query.all())

@app.route('/list_item', methods=['POST'])
def list_item():
    if request.method == 'POST':
        # Retrieve data from the form
        item_name = request.form['item_name']
        description = request.form['description']
        starting_bid = request.form['starting_bid']
        category_id = request.form['category']  # Get the selected category ID

        # Create a new item object with the selected category ID and add it to the database
        new_item = Item(name=item_name, description=description, starting_bid=starting_bid, category_id=category_id)
        db.session.add(new_item)
        db.session.commit()

        # Redirect to a success page or back to the account page
        return redirect(url_for('account'))

if __name__ == '__main__':
    app.run(debug=True)

from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, Response, session, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import UserMixin, LoginManager ,login_required, login_user, logout_user, current_user
from wtforms import StringField, IntegerField, FloatField, SubmitField, PasswordField 
from wtforms.validators import DataRequired, EqualTo, Email
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from threading import local


#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
_thread_local = local()

def get_db_conn():
    if not hasattr(_thread_local, 'db'):
        _thread_local.db = sqlite3.connect('database.db', check_same_thread=False)
    return _thread_local.db
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ACCOUNT_SID = "AC5f3438649249fe1846b7eeb665d857f3"
AUTH_TOKEN =  "4f0681635ed9847b6e4663cde5710af3"

client = Client(ACCOUNT_SID, AUTH_TOKEN)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Charlie_dont_surf1000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///managers.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mundane.db'
app.config['SQLALCHEMY_BINDS'] = {
    'managers': 'sqlite:///managers.db',
    'mundane': 'sqlite:///mundane.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------


# ================================================================================================

class users(db.Model, UserMixin):
    __bind_key__ = 'mundane'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class eusers(db.Model, UserMixin):
    __bind_key__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, code, email, password):
        self.name = name
        self.code = code
        self.email = email
        self.password = password

class executives(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Input a valid email')])
    code = IntegerField('Code', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords Must match!')])
    
    submit = SubmitField('Register Now😙!')

class mundanes(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Input a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords Must match!')])
    
    submit = SubmitField('Register Now😙!')

class mundane(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Input a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Save Changes!')

class mdn(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Input a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log In!')

class evt(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Input a valid email')])
    code = IntegerField('code', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log In!')
# ===================================================================================================
    
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def user(user_id):
    return users.query.get(int(user_id))

# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

@app.route('/admin', methods=['POST', 'GEt'])
def admin():
    id = current_user.id
    usr = users.query.get_or_404(id)
    all = users.query.order_by(users.date)
    if id == 1 or id== 4 or id == 5 or id == 8:
        flash(f'Welcome back {usr.name} 💕', category='success')
        return render_template('admin.html', all=all, name=usr.name)
    else:
        flash('Only admins can log in to this page')
        return redirect(url_for('home'))

@app.route('/e-login', methods=['GET', 'POST'])
def elogin():
    form = evt()

    if form.validate_on_submit():
        user = eusers.query.filter_by(email=form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data) and form.code.data == user.code:
                login_user(user)
                flash(f"Successful log in, Welcome back {user.name}", category='success')
                return redirect(url_for('home'))
            else:
                flash('Wrong Password mostly or wrong code! Kindly retry...', category='error')
                return render_template('elogin.html', form=form, id=user.id)
        
        else:
            flash(f"The email is not registered. Sign up for free below.", category='error')
            
    return render_template('elogin.html', form=form, id=0)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = mdn()

    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                response = make_response(redirect(url_for('home')))
                response.set_cookie('status', 'online')
                #st.session_state.status = 'online'
                flash(f"Successful log in, Welcome back {user.name}", category='success')
                return response
                
                #return redirect(url_for('home'))
            
            else:
                flash('Wrong Password! Kindly retry...', category='error')
                return render_template('login.html', form=form, id=user.id)
        
        else:
            flash(f"The email is not registered. Sign up for free below.", category='error')
            
    return render_template('login.html', form=form, id=0)


@app.route('/e-register', methods=['GET', 'POST'])
def eregister():
    name = None
    email = None
    password = None

    Xsr = None
    form = executives()

    if form.validate_on_submit():
        user = eusers.query.filter_by(email=form.email.data).first()
        if user:
            Xsr = user.name
            flash(f"{name}, Email already exist under the name {Xsr}! Choose another")
            return redirect(url_for('eregister'))
        else:
            user = eusers(name=form.name.data, code=form.code.data, email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            Xsr = user.name

            '''
            message = client.messages.create(
                    to= '+254794096950',
                    from_= '+12052363631',
                    body= f"Hope you enjoying your time LAWRENCE. Another Executive, name: {Xsr}, has ranked up!❤"
                )
            '''

        name = form.name.data
        email = form.email.data
        password = form.password.data

        form.email.data = ''
        form.password.data = ''
        
        flash(f'Your account has been successfully created {name}....Welcome❤', category="success")
        return redirect(url_for('home'))

    all = eusers.query.order_by(eusers.date)

    return render_template('esign.html', form=form, name=name, email=email, password=password, all=all)

@app.route('/register', methods=['GET', 'POST'])
def register():
    name = None
    email = None
    password = None
    Xsr = None
    form = mundanes()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user:
            Xsr = user.name
            flash(f"{name}, Email already exist under the name {Xsr}! Choose another")
            return redirect(url_for('register'))
        else:
            user = users(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            Xsr = user.name

            """
            message = client.messages.create(
                    to= '+254794096950',
                    from_= '+12052363631',
                    body= f"Hope you enjoying your time LAWRENCE. Another user, name: {Xsr}, has joined!❤"
                )
            """
        name = form.name.data
        email = form.email.data
        password = form.password.data

        form.email.data = ''
        form.password.data = ''
        
        flash(f'Your account has been successfully created {name}....Welcome❤', category="success")
        return redirect(url_for('home'))

    all = users.query.order_by(users.date)

    return render_template('sign.html', form=form, name=name, email=email, password=password, all=all)

@app.route('/e-update/<int:id>', methods=['GET', 'POST'])
def eupdate(id):
    form = executives()

    user = users.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.code = request.form['code']
        user.password = request.form['password']

        try:
            user.password = generate_password_hash(user.password, 'sha256')
            db.session.commit()
            flash(f"Changes applied successfully, {user.name}")
            return redirect(url_for('home'))
        except:
            flash("A problem occured, retry again")
            return render_template('updatee.html', form=form, user=user, id=id)    
    else:
        return render_template('updatee.html', form=form, user=user, id=id)  
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = mundane()

    user = users.query.get_or_404(id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']

        try:
            user.password = generate_password_hash(user.password, 'sha256')
            db.session.commit()
            flash(f"Changes applied successfully, {user.name}")
            return redirect(url_for('home'))
        
        except Exception as e:
            flash("A problem occured, retry again")
            return render_template('updatee.html', form=form, user=user, id=id)    
    else:
        return render_template('updatee.html', form=form, user=user, id=id)  

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    name = None
    email = None
    password = None
    form = executives()

    user = users.query.get_or_404(id)
    all = users.query.order_by(users.date)

    try:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.name} has been deleted successfully", category='success')
        return render_template('sign.html', form=form, name=name, email=email, password=password, all=all)
    except:
        flash("An error occured, retry again", category='error')
        return render_template('sign.html', form=form, name=name, email=email, password=password, all=all)


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    return redirect('http://localhost:8501')

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    id = current_user.id()
    user = users.query.get_or_404(id)
    logout_user()
    flash('you have been logged out.', category='success')

    if user:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('elogin'))


#                     000000 [[ --- BACKEND ENGINE --- FLK ]] 00000


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True) 
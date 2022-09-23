from flask import Flask, redirect, url_for, render_template, session, request
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
from springApiTest import getlist

app = Flask(__name__)

app.config['SECRET_KEY'] = '#$%^&*'


class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        return redirect('select')
    return render_template('index.html', form=form)


@app.route('/select', methods=['GET', 'POST'])
def select():
    print('session', session['startdate'])
    listss = getlist(session['startdate'])
    if request.method == 'POST':
        print(request.form.getlist('mycheckbox'))
        return 'Done'
    return render_template('select.html', listss=listss)

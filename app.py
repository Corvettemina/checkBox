from flask import Flask, redirect, url_for, render_template, session, request
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
from springApiTest import Springapi, copticDay

app = Flask(__name__)

app.config['SECRET_KEY'] = '#$%^&*'


class InfoForm(FlaskForm):
    startdate = DateField('Select Day For PowerPoint', format='%Y-%m-%d')
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
    spapi = Springapi(session['startdate'])
    #listss = spapi.getlist()["seasonVespersDoxologies"]
    if request.method == 'POST':

        spapi.dictionary["seasonVespersDoxologies"] = request.form.getlist(
            'seasonalDoxo')
        spapi.dictionary["optionalDoxogies"] = request.form.getlist(
            'optionalDoxo')

        print("Seasonal",  spapi.dictionary["seasonVespersDoxologies"])
        print("optional", spapi.dictionary["optionalDoxogies"])

        #import mergepptxaspose
        # mergepptxaspose()

        print('heyyyyy', request.form.getlist('seasonalDoxo'))
        return str(request.form.getlist('seasonalDoxo'))

    return render_template('select.html', spapi=spapi)

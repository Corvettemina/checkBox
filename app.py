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
    # listss = spapi.getlist()["seasonVespersDoxologies"]
    if request.method == 'POST':
        

        spapi.dictionary["seasonVespersDoxologies"] = request.form.getlist(
            'seasonalDoxoVespers')
        spapi.dictionary["vespersoptionalDoxogies"] = request.form.getlist(
            'optionalDoxoVespers')
            
        if ((request.form['bishopVespers']) == 'yes'):
            #spapi.dictionary["vespersoptionalDoxogies"].append("")
            spapi.dictionary["vespersPrayerofThanksgiving"] = "PowerPoints/BackBone/PrayerOfThanksgivingBishop.pptx"
            spapi.dictionary["vespersConclusion"] = "PowerPoints/BackBone/bishopConcludingHymn.pptx"

        if ((request.form['5short']) == 'no'):
            spapi.dictionary["vespers5ShortLitanies"] = ""

        spapi.dictionary["seasonmatinsDoxologies"] = request.form.getlist(
            'seasonalDoxoMatins')
        spapi.dictionary["matinsoptionalDoxogies"] = request.form.getlist(
            'optionalDoxoMatins')

        if ((request.form['5shortMatins']) == 'no'):
            spapi.dictionary["matins5ShortLitanies"] = ""

        import mergepptxaspose
        temp = mergepptxaspose.makeIntoList(spapi.dictionary)
        mergepptxaspose.merge(temp)

        #return str(request.form.getlist('seasonalDoxo'))

    return render_template('select.html', spapi=spapi)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

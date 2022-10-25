import string
from flask import Flask, redirect, url_for, render_template, session, request
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
from springApiTest import Springapi, copticDay
import platform
import subprocess

app = Flask(__name__)

app.config['SECRET_KEY'] = '#$%^&*'


class InfoForm(FlaskForm):
    startdate = DateField('Select Day For PowerPoint', format='%Y-%m-%d')
    submit = SubmitField('Submit')


def runDropbox():
    if (("Linux" in platform.platform())):
        result = subprocess.run(['dropbox', 'status'], stdout=subprocess.PIPE)
        stringResult = (result.stdout.decode('utf-8'))
        if ("running" in stringResult):
            subprocess.run(['service', 'dropbox', 'stop'],
                           stdout=subprocess.PIPE)
            subprocess.run(['dropbox', 'start'], stdout=subprocess.PIPE)


@app.route('/', methods=['GET', 'POST'])
def index():

    runDropbox()

    form = InfoForm()
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        return redirect('select')
    return render_template('index.html', form=form)


@app.route('/select', methods=['GET', 'POST'])
def select():
    print('session', session['startdate'])
    spapi = Springapi(session['startdate'])

    if request.method == 'POST':

        spapi.dictionary["seasonVespersDoxologies"] = request.form.getlist(
            'seasonalDoxoVespers')
        spapi.dictionary["vespersoptionalDoxogies"] = request.form.getlist(
            'optionalDoxoVespers')

        if ((request.form['bishopVespers']) == 'yes'):
            spapi.dictionary["vespersoptionalDoxogies"].append(
                "PowerPoints/BackBone/BishopDoxology.pptx")
            spapi.dictionary["vespersPrayerofThanksgiving"] = "PowerPoints/BackBone/PrayerOfThanksgivingBishopVespers.pptx"
            spapi.dictionary["vespersConclusion"] = "PowerPoints/BackBone/bishopConcludingHymn.pptx"

        if ((request.form['5short']) == 'no'):
            spapi.dictionary["vespers5ShortLitanies"] = ""

        spapi.dictionary["seasonmatinsDoxologies"] = request.form.getlist(
            'seasonalDoxoMatins')
        spapi.dictionary["matinsoptionalDoxogies"] = request.form.getlist(
            'optionalDoxoMatins')

        spapi.dictionary["thirdHourPsalms"] = request.form["3rdHourPsalm"]

        spapi.dictionary["sixthHourPsalms"] = request.form['6thHourPsalm']

        if ((request.form['5shortMatins']) == 'no'):
            spapi.dictionary["matins5ShortLitanies"] = ""

        spapi.dictionary["paralexHymns"] = request.form.getlist("paralexHymns")

        spapi.dictionary["prayerOfReconcilation"] = request.form.getlist(
            "prayerOfReconcilation")

        if ((request.form['rejoiceOMary']) == 'no'):
            spapi.dictionary["rejoiceOMary"] = ""

        if ((request.form['anaphora']) == 'Gregory'):
            spapi.dictionary["anaphora"] = "PowerPoints/Liturgy/Anaphora - Gregorian.pptx"

        if ((request.form['OLordofHosts']) == 'no'):
            spapi.dictionary["OLordofHosts"] = ""

        if ((request.form['agiosLiturgy']) == 'Gregory'):
            spapi.dictionary["agiosLiturgy"] = "PowerPoints/Liturgy/Agios - Gregorian.pptx"

        if ((request.form['instiution']) == 'Gregory'):
            spapi.dictionary["instiution"] = "PowerPoints/Liturgy/Institution - Gregorian.pptx"

        if ((request.form['yeahWeAskYou']) == 'no'):
            spapi.dictionary["yeahWeAskYou"] = ""

        if ((request.form['jeNaiNan']) == 'no'):
            spapi.dictionary["jeNaiNan"] = ""

        if ((request.form['Commemoration']) == 'Gregory'):
            spapi.dictionary["Commemoration"] = "PowerPoints/Liturgy/Commemoration - Gregorian.pptx"

        if ((request.form['postCommemoration']) == 'Gregory'):
            spapi.dictionary["postCommemoration"] = "PowerPoints/Liturgy/Post Commemoration - Gregorian.pptx"

        if ((request.form['prefaceToTheFraction']) == 'Gregory'):
            spapi.dictionary["prefaceToTheFraction"] = "PowerPoints/Liturgy/Preface - Gregorian.pptx"

        import mergepptxaspose
        temp = mergepptxaspose.makeIntoList(spapi.dictionary)

        mergepptxaspose.merge(temp)
        runDropbox()
        # return str(request.form.getlist('seasonalDoxo'))

    return render_template('select.html', spapi=spapi)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0')

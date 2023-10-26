
from flask import Flask, redirect, url_for, render_template, session, request, jsonify, Response
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from flask_cors import CORS
from wtforms import validators, SubmitField, RadioField
from springApiTest import Springapi, copticDay
import platform
import subprocess
import requests
import json
from datetime import datetime
from flask_bootstrap import Bootstrap
from wtforms import BooleanField
from wtforms.widgets import CheckboxInput
from threading import Thread
from collections import OrderedDict
import json
import certifi
import mergepptxaspose
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '#$%^&*'
app.config['GLOBAL_LIST'] = {}
 

class InfoForm(FlaskForm):
    toggle = BooleanField('Toggle')

    startdate = DateField('Select Day For PowerPoint', format='%Y-%m-%d')
    submit = SubmitField('Submit')


def merge(database, date):

    import mergepptxaspose

    paths = ["vespers","matins","offering","liturgyOfWord","liturgyOfFaithful","communion"]
    finalList = []
    for i in paths:
        finalList = finalList +  mergepptxaspose.makeIntoList(database[date][i], date)  

    for i in finalList:
        print (i)  
   
    mergepptxaspose.merge(finalList, date)

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

    response = requests.get('https://stmarkapi.com:8080/home', verify=False)
    y = json.loads(response.text)

    form = InfoForm()
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        print(session['startdate'])

        postResponse = requests.post('https://stmarkapi.com:8080/date?date=' + str(session['startdate']) , verify=False)
        print(postResponse.text)
        return redirect('select')
    return render_template('index.html', form=form, y=y)


@app.route('/vespers', methods=['GET', 'POST'])
def vespers():

    if request.method =='GET':
        return get('vespers')
    
    if request.method == 'POST':
        post('vespers')

        result = {'status': 'Vespers Updated'}
    
    return jsonify(result)
 
@app.route('/matins', methods=['GET', 'POST'])
def matins():
    if request.method =='GET':
    
        return get('matins')
    
    if request.method == 'POST':
        post('matins')

        result = {'status': 'Matins Updated'}
    
    return jsonify(result)
    
   

@app.route('/offering', methods=['GET', 'POST'])
def offering():

    if request.method =='GET':
        return get("offering")

    if request.method == 'POST':
        post('offering')

        result = {'status': 'Offering Updated'}
    
    return jsonify(result)

@app.route('/liturgyOfWord', methods=['GET', 'POST'])
def liturgyOfWord():
    if request.method =='GET':
        return get('liturgyOfWord')
    
    if request.method == 'POST':
        
        post('liturgyOfWord')

        result = {'status': 'Liturgy of the Word Updated'}
    
    return jsonify(result)


@app.route('/liturgyOfFaithful', methods=['GET', 'POST'])
def liturgyOfFaithful():

    if request.method =='GET':
        return get('liturgyOfFaithful')
    
    if request.method == 'POST':
        
        post('liturgyOfFaithful')

        result = {'status': 'Liturgy of the Faithful Updated'}
    
    return jsonify(result)


@app.route('/communion', methods=['GET', 'POST'])
def communion():

    if request.method =='GET':
        return get('communion')
        
    
    if request.method == 'POST':
        post('communion')
        result = {'status': 'Communion Updated'}
    
    return jsonify(result)

@app.route('/getAll', methods=['GET', 'POST'])
def getAll():

    if request.method =='GET':
        responsetoSend = {}
        try:
            (getLocal('vespers')["status"] ==  "No PPT For this date")
            responsetoSend["vespers"] = False
        except:
            responsetoSend["vespers"] = True

        try:
            (getLocal('matins')["status"] ==  "No PPT For this date")
            responsetoSend["matins"] = False
        except:
            responsetoSend["matins"] = True

        try:
            (getLocal('offering')["status"] ==  "No PPT For this date")
            responsetoSend["offering"] = False
        except:
            responsetoSend["offering"] = True

        try:
            (getLocal('liturgyOfWord')["status"] ==  "No PPT For this date")
            responsetoSend["liturgyOfWord"] = False
        except:
            responsetoSend["liturgyOfWord"] = True

        try:
            (getLocal('liturgyOfFaithful')["status"] ==  "No PPT For this date")
            responsetoSend["liturgyOfFaithful"] = False
        except:
            responsetoSend["liturgyOfFaithful"] = True

        try:
            (getLocal('communion')["status"] ==  "No PPT For this date")
            responsetoSend["communion"] = False
        except:
            responsetoSend["communion"] = True
        
        return jsonify(responsetoSend)
        


@app.route('/makeppt', methods=['GET', 'POST'])
def makePptx():
    date = request.args.get('date')
    if request.method == 'POST':
        try:
            filename = "data.json"
            with open(filename, "r") as json_file:
                database = json.load(json_file)
        except:
            database = {}

        if(database[date]["liturgyOfWord"]["synxar"] == "" ):
            postResponse = requests.get("https://stmarkapi.com:8080/liturgyOfWord?date=" + str(date) , verify=False)
            synxar = json.loads(postResponse.text)

            database[date]["liturgyOfWord"]["synxar"] = synxar[1]["synxar"]
        
        
        t = Thread(target=merge, args=(database, date))
        t.start()

    result = {'status': 'Powerpoint OTW'}
    
    return jsonify(result)


@app.route('/approval', methods=['GET', 'POST'])
def approval():
    date = request.args.get('date')
    if request.method == 'POST':
        try:
            filename = "data.json"
            with open(filename, "r") as json_file:
                database = json.load(json_file)
        except:
            print("HERE")
            database = {}
        import gmailTest
        gmailTest.gmail_send_message(date,database)
      
    result = {'status': 'sumbitted for approval'}
    
    return jsonify(result)

@app.route('/bishop', methods=['GET', 'POST'])
def bishop():
    date = request.args.get('date')
    if request.method == 'GET': 
        try:
            filename = "data.json"
            with open(filename, "r") as json_file:
                data = json.load(json_file)
        except:
            result = {'status': "Empty Database"}
            return jsonify(result)

        date = request.args.get('date')
        try:
            data[date]
        except:
            result = {'status': "No PPT For this date"}
            return jsonify(result)
                
        try:
            dataTosend = data[date]['vespers']['bishop']
            return jsonify({"bishop":dataTosend})
        
        except:
            result = {'status': "No Bishop option selected for this date"}
            return jsonify(result)  
    

def post(path):
    dataPosted = request.get_json()  

    try:
        filename = "data.json"
        with open(filename, "r") as json_file:
            data = json.load(json_file)
    except:
        data = {}

        #print(data)
    if request.args.get('date') in data:
        data[request.args.get('date')][path] = dataPosted
    else:
        data[request.args.get('date')] = {}
        data[request.args.get('date')][path] = dataPosted   

    with open(filename, "w") as json_file:
        json.dump( data , json_file)
    
def get(path):
    try:
        filename = "data.json"
        with open(filename, "r") as json_file:
            data = json.load(json_file)
    except:
        result = {'status': "Empty Database"}
        return jsonify(result)

    date = request.args.get('date')
    try:
        data[date]
    except:
        result = {'status': "No PPT For this date"}
        return jsonify(result)
        
    try:
        dataTosend = data[date][path]
        response_data = json.dumps(dataTosend, ensure_ascii=False, indent=4)
        response = Response(response_data, content_type='application/json')
        return response
    except:
        result = {'status': "No PPT For this date"}
        return jsonify(result)   

def getLocal(path):
    try:
        filename = "data.json"
        with open(filename, "r") as json_file:
            data = json.load(json_file)
    except:
        result = {'status': "Empty Database"}
        return (result)

    date = request.args.get('date')
    try:
        data[date]
    except Exception as e:
        result = {'status': "No PPT For this date"}
        return (result)
        
    try:
        return data[date][path]
    except Exception as e:
        
        result = {'status': "No PPT For this date"}
        return (result) 
      
def convert_date_format(date_str):
    dt = datetime.strptime(date_str, '%Y-%b-%d')

    new_date_str = dt.strftime('%Y-%m-%d')

    return new_date_str

@app.route('/select', methods=['GET', 'POST'])
def select():
    form = InfoForm()
    print('Session', session['startdate'])
    spapi = Springapi( session['startdate'])

    start_date_str = session['startdate']
    start_date = datetime.strptime(start_date_str, "%a, %d %b %Y %H:%M:%S %Z")
    start_date = start_date.strftime("%A, %b %d, %Y")

    if request.method == 'POST':
        #print(form.toggle.data)

        #print(request.form['toggle'])

        spapi.dictionary["seasonVespersDoxologies"] = request.form.getlist(
            'seasonalDoxoVespers')
        spapi.dictionary["vespersoptionalDoxogies"] = request.form.getlist(
            'optionalDoxoVespers')
        '''
        if ((request.form['bishopVespers']) == 'yes'):
            spapi.dictionary["vespersoptionalDoxogies"].append(
                "PowerPoints/BackBone/BishopDoxology.pptx")
            spapi.dictionary["vespersPrayerofThanksgiving"] = "PowerPoints/BackBone/PrayerOfThanksgivingBishopVespers.pptx"
            spapi.dictionary["vespersConclusion"] = "PowerPoints/BackBone/bishopConcludingHymn.pptx"
        '''
        if ((request.form['vespersGospelLitany']) == 'yes'):
            spapi.dictionary["vespersLitanyofTheGospel"] = "PowerPoints/BackBone/AnotherLitanyOftheGospel.pptx"

        if ((request.form['5short']) == 'no'):
            spapi.dictionary["vespers5ShortLitanies"] = ""

        spapi.dictionary["seasonmatinsDoxologies"] = request.form.getlist(
            'seasonalDoxoMatins')
        spapi.dictionary["matinsoptionalDoxogies"] = request.form.getlist(
            'optionalDoxoMatins')


        if ((request.form['matinsGospelLitany']) == 'yes'):
            spapi.dictionary["matinsLitanyofTheGospel"] = "PowerPoints/BackBone/AnotherLitanyOftheGospel.pptx"

        if ((request.form['5shortMatins']) == 'no'):
            spapi.dictionary["matins5ShortLitanies"] = ""

        spapi.dictionary["thirdHourPsalms"] = request.form["3rdHourPsalm"]

        spapi.dictionary["sixthHourPsalms"] = request.form['6thHourPsalm']

        spapi.dictionary["paralexHymns"] = request.form.getlist("paralexHymns")

        if ((request.form['liturgyGospelLitany']) == 'yes'):
            spapi.dictionary["LiturgylitanyoftheGospel"] = "PowerPoints/BackBone/litanyofthegospel.pptx"

        if ((request.form['Liturgy3GreatLitanies']) == 'no'):
            spapi.dictionary["Liturgy3GreatLitanies"] = ""

        spapi.dictionary["prayerOfReconcilation"] = request.form["prayerOfReconcilation"]

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

        if ((request.form['healingToThesick']) == 'no'):
            spapi.dictionary["healingToThesick"] = ""

        if ((request.form['Commemoration']) == 'Gregory'):
            spapi.dictionary["Commemoration"] = "PowerPoints/Liturgy/Commemoration - Gregorian.pptx"

        if ((request.form['postCommemoration']) == 'Gregory'):
            spapi.dictionary["postCommemoration"] = "PowerPoints/Liturgy/Post Commemoration - Gregorian.pptx"

        if ((request.form['prefaceToTheFraction']) == 'Gregory'):
            spapi.dictionary["prefaceToTheFraction"] = "PowerPoints/Liturgy/Preface - Gregorian.pptx"

        spapi.dictionary["seasonalFraction"] = request.form["seasonalFraction"]

        spapi.dictionary["fractionIndex"] = request.form["fractionIndex"]

        spapi.dictionary["communionHymns"] = request.form.getlist("communionHymns")
        spapi.dictionary["AllCommunionHymns"] = request.form.getlist("AllCommunionHymns")

        import mergepptxaspose
        temp = mergepptxaspose.makeIntoList(spapi.dictionary)
        for i in temp:
            print(i)
        t = Thread(target=merge, args=(temp,))
        t.start()
        #mergepptxaspose.merge(temp)

        runDropbox()
        return redirect('finalScreen')

        # return str(request.form.getlist('seasonalDoxo'))

    return render_template('select.html', spapi=spapi, start_date=start_date, form=form)


if __name__ == "__main__":
    #app.run(debug=True)
    #app.run(host='0.0.0.0')
    
    app.run(host='0.0.0.0',ssl_context=('/etc/letsencrypt/archive/stmarkapi.com/cert1.pem', '/etc/letsencrypt/archive/stmarkapi.com/privkey1.pem'))

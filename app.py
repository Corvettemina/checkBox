
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
import logging
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

app.logger.setLevel(logging.DEBUG)
months ={"01" : "January",
         "02" : "February",
         "03" : "March",
         "04" : "April",
         "05" : "May",
         "06" : "June",
         "07" : "July",
         "08" : "August",
         "09" : "September",
         "10" : "October",
         "11" : "November",
         "12" : "December"}

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


@app.route('/<section>', methods=['GET', 'POST'])
def getSection(section):

    if request.method =='GET':
        return get(section)
    
    if request.method == 'POST':
        post(section)

        result = {'status': f'{section} Updated'}
    
    return jsonify(result)
 

@app.route('/getAll', methods=['GET', 'POST'])
def getAll():

    listOfSections = ['vespers','matins','offering','liturgyOfWord','liturgyOfFaithful','communion']
    if request.method =='GET':
        responsetoSend = {}
        for i in listOfSections:
            try:
                (getLocal(i)["status"] ==  "No PPT For this date")
                responsetoSend[i] = False
            except:
                responsetoSend[i] = True

        return jsonify(responsetoSend)
        


@app.route('/makeppt', methods=['GET', 'POST'])
def makePptx():
    date = request.args.get('date')

    readingsString = request.args.get('readingsDate')
   
    if request.method == 'POST':
        try:
            filename = "data.json"
            with open(filename, "r") as json_file:
                database = json.load(json_file)
        except:
            database = {}
        if(date in database.keys()):

            if readingsString:
                    readings = readingsString.split("-")
                    year = readings[0]
                    month = readings[1]
                    day = readings[2]
                    
                    newReadingsString = "Readings/" + year + "/" + month + months[month] + "/" + str(int(day) - 1) + "-" + year + "-" + months[month][:3].lower() + "-" + str(int(day)) + "/"

                    database[date]["vespers"]["vespersGospel"] = newReadingsString + "Vespers Gospel.pptx"
                    database[date]["matins"]["matinsGospel"] = newReadingsString + "Matins Gospel.pptx"
                    database[date]["liturgyOfWord"]["pauline"][0] = newReadingsString + "Pauline.pptx"
                    database[date]["liturgyOfWord"]["catholic"] = newReadingsString + "Catholic.pptx"
                    database[date]["liturgyOfWord"]["acts"] = newReadingsString + "Acts.pptx"
                    database[date]["liturgyOfWord"]["LiturgyPsalm"] = newReadingsString + "LiturgyPsalm.pptx"
                    database[date]["liturgyOfWord"]["LiturgyGospel"] = newReadingsString + "LiturgyGospel.pptx"
            
            if(database[date]["liturgyOfWord"]["synxar"] == "" ):
                postResponse = requests.get("https://stmarkapi.com:8080/liturgyOfWord?date=" + str(date) , verify=False)
                synxar = json.loads(postResponse.text)

                database[date]["liturgyOfWord"]["synxar"] = synxar[1]["synxar"]
            
            
            t = Thread(target=merge, args=(database, date))
            t.start()

            if(readingsString):
                result = {'status': 'Powerpoint OTW' , 'Readings date:' : readingsString}
            else:
                result = {'status': 'Powerpoint OTW'}
        else:
            result = {'status': 'No Powerpoint For that Date'}

    if request.method == 'GET':
        result = {'status' : 'POST ONLY METHOD'}

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
    
    if request.method == 'GET':
        result = {'status' : 'POST ONLY METHOD'}
        
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
    app.run(debug=True)
    #app.run(host='0.0.0.0')
    
    #app.run(host='0.0.0.0',ssl_context=('/etc/letsencrypt/archive/stmarkapi.com/cert6.pem', '/etc/letsencrypt/archive/stmarkapi.com/privkey6.pem'))

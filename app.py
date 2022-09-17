from flask import Flask, render_template, request
import springApiTest

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    listss = springApiTest.getlist()
    if request.method == 'POST': 
        print(request.form.getlist('mycheckbox'))
        return 'Done'
    return render_template('index.html', listss = listss)
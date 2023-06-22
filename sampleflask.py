from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
import pytesseract
import cv2

 
#*** Backend operation
 
# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
 
 
@app.route('/')
def index():
    return render_template('home.html')
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
 
        return render_template('home1.html')
 
@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    txt=pytesseract.image_to_string(cv2.imread(img_file_path),lang="aze")
    txtprod=pytesseract.image_to_string(cv2.imread(img_file_path)[300:-640,:185])
    txtquant=pytesseract.image_to_string(cv2.imread(img_file_path)[:,185:],lang="aze")
    tot=[]
    start=0
    end=0
    new=[]
    quantity=[]
    for i,j in enumerate(list(filter(None,txtquant.split('Cəmi')[1].split('\n')))):
        if len(j.split(')')[-1].strip().split(' '))==3:
            quantity.append(j.split(')')[-1].strip())
    for i,j in enumerate(txtprod.split('\n')):
        if '18' in j or 'azad' in j.lower():
            end=i
            new.append(''.join(txtprod.split('\n')[start+1:end]))
        start=end

    new=list(filter(None,new))
    for i in range(len(list(filter(None,new)))):
        c=[]
        c={'prodName':new[i],
        'quantity':float(quantity[i].split(' ')[0].replace(':','.'))/1000 if ',' not in quantity[i].split(' ')[0].replace(':','.') and len(quantity[i].split(' ')[0].replace(':','.'))!=1 and '.' not in quantity[i].split(' ')[0].replace(':','.') else quantity[i].split(' ')[0].replace(':','.'),
        'price':float(quantity[i].split(' ')[1].replace(':','.'))/1000 if len(quantity[i].split(' ')[1].replace(':','.'))==4 and ',' not in quantity[i].split(' ')[1].replace(':','.') and '.' not in quantity[i].split(' ')[1].replace(':','.') else float(quantity[i].split(' ')[1].replace(':','.'))/100 if len(quantity[i].split(' ')[1].replace(':','.'))==3 and ',' not in quantity[i].split(' ')[1].replace(':','.') and '.' not in quantity[i].split(' ')[1].replace(':','.') else float(quantity[i].split(' ')[1].replace(':','.'))/10 if len(quantity[i].split(' ')[1].replace(':','.'))==2 and ',' not in quantity[i].split(' ')[1].replace(':','.') and '.' not in quantity[i].split(' ')[1].replace(':','.') else float(quantity[i].split(' ')[1].replace(':','.')) ,
        'total': float(quantity[i].split(' ')[2].replace(':','.'))/1000 if len(quantity[i].split(' ')[2].replace(':','.'))==4 and ',' not in quantity[i].split(' ')[2].replace(':','.') and '.' not in quantity[i].split(' ')[2].replace(':','.') else float(quantity[i].split(' ')[2].replace(':','.'))/100 if len(quantity[i].split(' ')[2].replace(':','.'))==3 and ',' not in quantity[i].split(' ')[2].replace(':','.') and '.' not in quantity[i].split(' ')[2].replace(':','.') else float(quantity[i].split(' ')[2].replace(':','.'))/10 if len(quantity[i].split(' ')[2].replace(':','.'))==2 and ',' not in quantity[i].split(' ')[2].replace(':','.') and '.' not in quantity[i].split(' ')[2].replace(':','.') else float(quantity[i].split(' ')[2].replace(':','.'))}
        tot.append(c)

    dictionary1={'shop':txt.split('\n')[0].split(': ')[1],
                'transactionDate':txt.lower().split('tarix:')[1].strip().split(' ')[0].split('\n')[0]+' '+txt.lower().split('vaxt:')[1].strip().split(' ')[0].split('\n')[0],
                'checkNo':txt.split('\n')[10].split(' ')[-1],
                'products':tot,
                }
    for i in range(len(dictionary1['products'])):
        dictionary1['products'][i]['total']=round(float(dictionary1['products'][i]['quantity'])*float(dictionary1['products'][i]['price']),3)
    dictionary1
    
    return render_template('show_image.html', user_image = dictionary1)


if __name__ == "__main__":
    import random, threading, webbrowser

    port = 5000 + random.randint(0, 999)
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

    app.run(port=port, debug=False)
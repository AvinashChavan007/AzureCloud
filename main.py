from flask import Flask,render_template,request
from flaskext.mysql import MySQL
from azure.storage.blob import BlockBlobService,ContentSettings
import datetime
from base64 import b64encode

app = Flask(__name__)

mysql = MySQL()
#mysql credentials
app.config['MYSQL_DATABASE_USER'] = '<your db user>'
app.config['MYSQL_DATABASE_PASSWORD'] = '<your db password>'
app.config['MYSQL_DATABASE_DB'] = '<your database name>'
app.config['MYSQL_DATABASE_HOST'] = '<your db host name>'

mysql.init_app(app)
block_blob_service = BlockBlobService(account_name='azureassignstorage', account_key='Em/Z0Apr8Ne7sOq927X5I/BRWdctDYvzRCSWeTzavyBjDrDSdTbG2ki2dij5AVEw37cWFd1AVlFTg0qMIwICew==')
storage_name = "http://azureassignstorage.blob.core.windows.net/imagefiles/"
username =""
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    return render_template("dashboard.html",msg=username)


@app.route("/uploadpage")
def uploadpage():
username
    return render_template("upload.html",msg=username)

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo

@app.route("/viewpage")
def showFile():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from image_blob")
    imagedata = []
    conn.close()
    data = cursor.fetchall()
    for row in data:
        print(row)
        imagedata.append(row)
    return render_template("view.html",imgagefile = imagedata)

@app.route("/viewfromdatabase")
def viewfromdatabase():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select image_title,image_owner,image_name,hex(image) as image,created_date,rating from image")
    imagedata = []
    datafile = []
    conn.close()
    data = cursor.fetchall()
    for row in data:
        imagedata.append(row[0])
        imagedata.append(row[1])
        imagedata.append(row[2])
        imagedata.append(str(b64encode(bytes.fromhex(row[3])))[2:-1])
        imagedata.append(row[4])
        imagedata.append(row[5])
        datafile.append(imagedata)
    return render_template("viewfromdata.html",imgagefile = datafile)

@app.route('/upload', methods=['POST'])
def upload():
        """Process the uploaded file and upload it to Google Cloud Storage."""
        uploaded_file = request.files['file']
        data = read_file('C:\\Users\\chvna\\Desktop\\Data\DP\\'+uploaded_file.filename)
        imagename = uploaded_file.filename
        author = request.form['fileauthor']
        title = request.form['filetitle']
        rating = request.form['inputstart']
        today = datetime.datetime.now()
        conn = mysql.connect()
        cursor = conn.cursor()
        add_image = ("INSERT INTO image(image_title,image_owner,image_name,image,created_date,rating) VALUES (%s, %s, %s, %s, %s, %s);")
        data_image = (title,author, imagename,data,today,int(rating))
        cursor.execute(add_image, data_image)
        conn.commit()
        return render_template("upload.html",success = "File Uploaded SuccessFully")

@app.route('/uploadtostorage', methods=['POST'])
def uploadtostorage():
        # Upload File to Blob
        uploaded_file = request.files['file1']
        block_blob_service.create_blob_from_path(
                'imagefiles',
                 uploaded_file.filename,
                'C:\\Users\\chvna\\Desktop\\Data\DP\\'+uploaded_file.filename,
                content_settings=ContentSettings(content_type='image/png')
        )

        imagename = uploaded_file.filename
        author = request.form['fileauthor1']
        title = request.form['filetitle1']
        rating = request.form['inputstar']
        today = datetime.datetime.now()
        conn = mysql.connect()
        cursor = conn.cursor()
        add_image = ("INSERT INTO image_blob(image_title,image_owner,image_name,image,created_date,rating) VALUES (%s, %s, %s, %s, %s, %s);")
        data_image = (title,author, imagename,storage_name+uploaded_file.filename,today,int(rating))
        cursor.execute(add_image, data_image)
        conn.commit()
        return render_template("upload.html",success1 = "File Uploaded SuccessFully")

if __name__ == '__main__':
    app.run(debug=True)
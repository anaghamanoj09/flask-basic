from flask import Flask,render_template,request,redirect,url_for,session,flash,jsonify
from dbconnection.datamanipulation import *
from werkzeug.utils import secure_filename
import os 

ind=Flask(__name__)
ind.secret_key="highsecretkey"
upload_folder="./static"

ind.config["UPLOAD_FOLDER"]=upload_folder
ind.config["MAX-CONTENT_LENGTH"]=16*1024*1024

ALLOWED_EXTENSIONS={'jpg','png','PNG'}

def allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@ind.route("/")
def index():
    return render_template("index.html")

@ind.route("/register")
def register():
    return render_template("register.html")

@ind.route("/regAction",methods=['post'])
def regAction():
    name=request.form['name']
    age=request.form['age']
    address=request.form['address']
    username=request.form['username']
    password=request.form['password']
    sql_edit_insert("insert into stdreg_tb values(NULL,?,?,?,?,?)",(name,age,address,username,password))
    flash("Registrartion successfull")
    return redirect(url_for('register'))

@ind.route("/login")
def login():
    return render_template("login.html")

@ind.route("/std_loginAction",methods=['post'])
def std_loginAction():
    username=request.form['username']
    password=request.form['password']
    data=sql_query2("select * from stdreg_tb where Username=? and Password=?",(username,password))
    if len(data)>0:
        session['stdid']= data[0][0]
        flash("login successfull")
        return render_template("home.html")
    else:
        return redirect(url_for('login'))

@ind.route("/view_std")
def view_std():
    std=sql_query("select * from stdreg_tb")
    return render_template("view_std.html",us=std)   

@ind.route("/edit")
def edit():
    studentid=request.args.get('stdid')
    std=sql_query2("select * from stdreg_tb where id=?",(studentid))
    return render_template("edit.html",us=std)

@ind.route("/std_editaction",methods=['post'])
def std_editaction():
    id=request.form['id']
    name=request.form['name']
    age=request.form['age']
    address=request.form['address']
    username=request.form['username']
    sql_edit_insert("update stdreg_tb set Name=?,Age=?,Address=?,Username=? where id=?",(name,age,address,username,id))
    flash("updated")
    return redirect(url_for('view_std'))

@ind.route("/delete")
def delete():
    studentdid=request.args.get('stdid')
    sql_edit_insert("delete from stdreg_tb where id=?",(studentdid))
    flash("deleted")
    return redirect(url_for('view_std'))

@ind.route("/view_profile")
def view_profile():
    user=session['stdid']
    std=sql_query2("select * from stdreg_tb where id=?",[user])
    return render_template('view_profile.html',us=std)

@ind.route("/dropdown_country")
def dropdown_country():
    std=sql_query("select * from country")
    return render_template('dropdown_country.html',us=std)

@ind.route("/Image_upload")
def Image_upload():
    return render_template("Image_upload.html")

@ind.route("/file_upload",methods=["post"])
def file_upload():
    if len(request.files)>0:
        file=request.files['image']
    if file and allowed(file.filename):
        filename=secure_filename(file.filename)
        r=sql_edit_insert("insert into image_tb values(NULL,?,?)",(request.form['name'],filename))
    if(r>0):
        file.save(os.path.join(ind.config["UPLOAD_FOLDER"],filename))
        return redirect(url_for("Image_upload"))
    return redirect(url_for("Image_upload"))

@ind.route("/get_username")
def get_username():
    std=request.args.get('name')
    data=sql_query2("select * from stdreg_tb where Username=?",[std])
    if len(data)>0:
        msg="exist"
    else:
        msg="not exist"
    print(msg)
    return jsonify({'valid':msg})


if __name__ == "__main__":
    ind.run(debug=True)